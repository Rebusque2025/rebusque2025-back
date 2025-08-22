from flask import Blueprint, render_template, jsonify, url_for,request
import os
from src.models import db, User, UserRole
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy import select


# Define a new Blueprint for the API
main = Blueprint('api', __name__)

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
        password = data.get("password")
        role = data.get("role")   # "cliente" o "proveedor"
        photo_url = data.get("photo_url")

        # Validaciones básicas
        if not name or not email or not password or not role:
            return jsonify({"msg": "Name, email, password and role are required"}), 400

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
        access_token = create_access_token(identity=query_user.id)

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