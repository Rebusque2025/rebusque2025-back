from flask import Blueprint, render_template, jsonify, url_for, request
import os
from src.models import db, User, Category, Service, Contract, Review
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func


# Define a new Blueprint for the API
main = Blueprint('api', __name__)
search_bp = Blueprint('search', __name__)

@main.route('/')
def index():
    # Obtiene la URL base de tu archivo .env
    base_url = os.getenv('BASE_URL')
    
    # Usa url_for para generar la URL del admin
    admin_url = url_for('admin.index')
    
    # Combina la URL base con la URL del admin
    # Esto es opcional si solo necesitas la URL generada por url_for
    full_admin_url = f"{base_url}{admin_url}" if base_url else admin_url
    
    # Renderiza la plantilla, pasando la URL del admin
    return render_template('index.html', admin_url=full_admin_url)

@main.route('/users', methods=['GET'])
def get_users():
    # Consulta todos los usuarios desde la base de datos
    # users = User.query.all()

    # Convierte los usuarios a una lista de diccionarios
    # para que puedan ser serializados a JSON
    # users_list = []
    # for user in users:
    #     users_list.append({
    #         'id': user.id,
    #         'username': user.username,
    #         'email': user.email
    #     })

    # Devuelve la lista en formato JSON
    return jsonify({"msg": "conectado"})

@main.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        role = data.get("role")   # "cliente" o "proveedor"
        photo_url = data.get("photo_url")

        # Validaciones básicas
        if not name or not email or not phone or not password or not role:
            return jsonify({"msg": "Name, email, phone, password and role are required"}), 400

        # Validar que el role sea correcto
        if role not in ["cliente", "proveedor"]:
            return jsonify({"msg": "Role must be 'cliente' or 'proveedor'"}), 400

        # Verificar si el usuario ya existe
        existing_user = db.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

        if existing_user:
            return jsonify({"msg": "User already exists"}), 409

        # Crear nuevo usuario con contraseña hasheada
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password),
            role=role,  # guardamos como string directamente
            photo_url=photo_url,
            is_active=True
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "msg": "User created successfully",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "phone": new_user.phone,
                "role": new_user.role,
                "photo_url": new_user.photo_url
            }
        }), 201

    except Exception as e:
        print(f"error: {e}")
        return jsonify({"msg": "Unexpected error"}), 500


@main.route("/login", methods=["POST"])
def login():
    try:
        email = request.json.get("email")
        password = request.json.get("password")

        if not email or not password:
            return jsonify({"msg": "Email and password are required"}), 400

        # Buscar usuario por email
        query_user = db.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

        if query_user is None:
            return jsonify({"msg": "User does not exist"}), 404

        # Verificar contraseña con hash
        if not check_password_hash(query_user.password, password):
            return jsonify({"msg": "Bad email or password"}), 401

        # Generar token con ID del usuario
        access_token = create_access_token(identity=str(query_user.id)) ### parseando a string el id

        return jsonify({
            "msg": "Login successful",
            "access_token": access_token,
            "user": {
                "id": query_user.id,
                "name": query_user.name,
                "email": query_user.email,
                "role": query_user.role,  # ya es string
                "photo_url": query_user.photo_url
            }
        }), 200

    except Exception as e:
        print(f"error: {e}")
        return jsonify({"msg": "Unexpected error"}), 500

@main.route("/search/professionals", methods=["GET"])
def search_professionals():
    query = request.args.get("q", None)

    if not query:
        return jsonify({"msg": "Query parameter 'q' is required"}), 400

    role_value = "proveedor"  # string literal

    # Consulta uniendo User, Service y Category
    results = (
        db.session.query(User)
        .join(Service)
        .join(Category)
        .filter(
            User.role == role_value,  # aquí usamos string puro
            or_(
                User.name.ilike(f"%{query}%"),
                User.phone.ilike(f"%{query}%"),
                Service.title.ilike(f"%{query}%"),
                Service.description.ilike(f"%{query}%"),
                Category.name.ilike(f"%{query}%")
            )
        )
        .all()
    )

    # Serializamos los resultados
    response = []
    for u in results:
        response.append({
            "services": [
                {
                    "title": s.title,
                    "description": s.description,
                    "price": s.price,
                    "category": s.category.name
                }
                for s in u.services
            ]
        })

    return jsonify(response), 200

####### Enpoints filtros #######

#GET de todas las categorias
@main.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

# Barra de filtro de busqueda con bp aparte 

@search_bp.route("/search", methods=["GET"])
def search_services():

       #### Filtros categoria, precio, rating y status 
    category_id = request.args.get("category_id", type=int)
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    min_rating = request.args.get("min_rating", type=float)
    contract_status = request.args.get("status", type=str)

    query = Service.query

    if category_id:
        query = query.filter(Service.category_id == category_id)

    if min_price is not None:
        query = query.filter(Service.price >= min_price)

    if max_price is not None:
        query = query.filter(Service.price <= max_price) 

    if contract_status:
        query = query.join(Service.contracts).filter(Contract.status == contract_status).group_by(Service.id)

    if contract_status:
        query = query.join(Service.contracts).filter(Contract.status == contract_status)

#### rating promedio
    if min_rating is not None:
        query = query.join(Service.contracts).join(Contract.reviews).group_by(Service.id)
        query = query.having(func.avg(Review.rating) >= min_rating)
        
    services = query.all()

    result = [
        {
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "price": s.price,
            "provider": s.provider.name,
            "category": s.category.name,
            "contracts": [
                {
                    "id": c.id,
                    "start_date": c.start_date,
                    "status": c.status
                }
                for c in s.contracts if not contract_status or c.status == contract_status
            ],
            "average_rating": db.session.query(func.coalesce(func.avg(Review.rating), 0)).join(Service.contracts).outerjoin(Contract.reviews).filter(Service.id == s.id).scalar()
        }
        for s in services
    ]

    return jsonify(result)

@search_bp.route("/provider/<int:user_id>/services", methods=["GET"])
def get_provider_services(user_id):

    services = Service.query.filter_by(provider_id=user_id).all()
    print(services[0].contracts)
    result = [
        {
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "price": s.price,
            "photo_url": s.photo_url,
            "contracts": [
                {
                    "id": c.id,
                    "client_name": c.client.name if c.client else None,
                    "status": c.status,
                    "start_date": c.start_date
                }
                for c in s.contracts if c.status in ["en curso", "entregado"]
            ]
        }
        for s in services
    ]

    return jsonify(result)

@search_bp.route("/client/contracts", methods=["GET"])
@jwt_required()
def get_client_contracts():
    current_user_id = int(get_jwt_identity())

    contracts = Contract.query.filter_by(client_id=current_user_id).all()

    print(contracts)
    result = [
        c.serialize()
        for c in contracts
        if c.status in ["esperando confirmación", "completado"]
    ]

    return jsonify(result)


#####anexar endpoit de auth

@main.route("/valid-auth", methods=["GET"])
@jwt_required()
def valid_auth():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify(error="Usuario no encontrado"), 404

    return jsonify( logged=True, logged_in_as=user.email, logged_in_phone=user.phone, role=user.role), 200


##### Endpoint POST de solicitud de servicio/contrato de un usuario cliente logueado y autorizado ######

@search_bp.route("/contracts", methods=["POST"])
@jwt_required()
def create_contract():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()

    service_id = data.get("service_id")
    if not service_id:
        return jsonify({"error": "service_id es requerido"}), 400

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "servicio no encontrado"}), 404

    provider_id = service.provider_id

    new_contract = Contract(
        client_id=current_user_id,
        provider_id=provider_id,
        service_id=service_id,
        status="esperando confirmación"
    )
    db.session.add(new_contract)
    db.session.commit()

    return jsonify({
        "msg": "Contrato creado exitosamente",
        "contract": {
            "id": new_contract.id,
            "service": service.title,
            "provider": {
                "id": provider_id,
                "name": service.provider.name
            },
            "status": new_contract.status,
            "start_date": new_contract.start_date

        }
    }), 201



   
