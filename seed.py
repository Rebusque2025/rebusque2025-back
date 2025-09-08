import random
from datetime import datetime, timedelta
from faker import Faker
from app import app, db
from src.models import User, Category, Service, Contract, Review

# Inicializa Faker
fake = Faker('es_ES')

def seed_database():
    """
    Función principal para poblar la base de datos con datos de prueba.
    """
    with app.app_context():
        # Elimina los datos existentes
        db.drop_all()
        db.create_all()

        print("🚀 Creando datos de prueba...")

        # 1. Crear usuarios fijos y aleatorios
        users = []

        # Usuarios fijos de tu base de datos
        users.append(User(name="Daniela", last_name="Eula", email="daniela@gmail.com", phone="888888888", password="password", role="proveedor"))
        users.append(User(name="Carlos", last_name="Lorenzo", email="carlos@gmail.com", phone="777777777", password="password", role="cliente"))
        users.append(User(name="Eduardo", last_name="Valverde", email="eduardo@gmail.com", phone="666666666", password="password", role="cliente"))
        users.append(User(name="Mariam", last_name="Duarte", email="mduarte@email.com", phone="+34612345789", password="password", role="proveedor"))
        users.append(User(name="Judith", last_name="Ramírez Pachón", email="judith@email.com", phone="+34639528417", password="password", role="proveedor"))

        # Crear usuarios aleatorios para completar la base de datos
        for _ in range(15):
            # Genera un correo electrónico o un teléfono
            if random.choice([True, False]):
                email = fake.unique.email()
                phone = None
            else:
                email = None
                phone = fake.unique.phone_number()
            
            user = User(
                name=fake.first_name(),
                last_name=fake.last_name(),
                email=email,
                phone=phone,
                password="password",
                role=random.choice(["proveedor", "cliente"]),
                photo_url=fake.image_url(),
                is_active=True,
                average_rating=0.0,
                total_reviews=0
            )
            users.append(user)

        db.session.add_all(users)
        db.session.commit()
        print(f"✔️ {len(users)} usuarios creados.")

        # 2. Crear categorías fijas
        categories = []
        fixed_categories = ["Plomería", "Electricidad", "Carpintería", "Jardinería", "Limpieza",
                            "Pintura", "Fontanería", "Mecánica", "Cerrajería", "Informática",
                            "cuidado de mayores", "cuidado infantil", "albañilería", "decoración", "cocina", "piscinas"]
        for cat_name in fixed_categories:
            category = Category(name=cat_name)
            categories.append(category)
        db.session.add_all(categories)
        db.session.commit()
        print(f"✔️ {len(categories)} categorías de servicio creadas.")

        # 3. Crear servicios fijos y aleatorios
        services = []
        providers_dict = {u.name: u for u in users if u.role == "proveedor"}
        categories_dict = {c.name: c for c in categories}
        
        # Servicios fijos basados en tu base de datos
        service1 = Service(
            title="Limpieza profunda",
            description="Tu hogar más limpio que nunca. Puedo ir a hacer limpieza general semanalmente o a realizar una limpieza en profundidad. ¡Contáctame!",
            price=35.0,
            provider=providers_dict['Daniela'],
            category=categories_dict['Limpieza']
        )
        services.append(service1)

        service2 = Service(
            title="Pinta tu casa",
            description="15 años de experiencia pintando todo tipo de paredes para que vuelvas a sentir tu hogar limpio, nuevo y acogedor.",
            price=250.0,
            provider=providers_dict['Mariam'],
            category=categories_dict['Pintura']
        )
        services.append(service2)
        
        service3 = Service(
            title="Carpintería Dani",
            description="Todo tipo de trabajo con madera: restauraciones, muebles personalizados, parqués...",
            price=80.0,
            provider=providers_dict['Judith'],
            category=categories_dict['Carpintería']
        )
        services.append(service3)

        # Crear servicios aleatorios para los demás proveedores
        for provider in providers_dict.values():
            if provider.name not in ["Daniela", "Mariam", "Judith"]:
                for _ in range(random.randint(1, 2)):
                    service = Service(
                        title=f"{random.choice(['Servicio de', 'Trabajo de'])} {random.choice(list(categories_dict.keys()))}",
                        description=fake.paragraph(nb_sentences=5),
                        price=round(random.uniform(20.0, 500.0), 2),
                        provider=provider,
                        category=random.choice(categories)
                    )
                    services.append(service)

        db.session.add_all(services)
        db.session.commit()
        print(f"✔️ {len(services)} servicios creados.")

        # 4. Crear contratos y reseñas que reflejen tu base de datos
        contracts = []
        clients = [u for u in users if u.role == "cliente"]
        clients_dict = {u.name: u for u in clients}
        
        # Contrato 1: Completado con reseña
        # Seleccionamos un servicio de "Carpintería" para el contrato
        carpinteria_service = next(s for s in services if s.title.startswith("Carpintería"))

        contract1 = Contract(
            start_date=datetime.utcnow() - timedelta(days=5),
            status="completado",
            client=clients_dict['Carlos'],
            provider=providers_dict['Judith'],
            service=carpinteria_service
        )
        contracts.append(contract1)
        db.session.add(contract1)
        db.session.commit() 
        
        review1 = Review(
            rating=4,
            comment="Hizo un trabajo excelente con la puerta, pero al barniz se le notan algunos goterones",
            created_at=datetime.utcnow(),
            contract=contract1,
            author=contract1.client,
            recipient=contract1.provider
        )
        db.session.add(review1)

        # Actualizar rating del proveedor
        provider = contract1.provider
        provider.total_reviews += 1
        provider.average_rating = ((provider.average_rating * (provider.total_reviews - 1)) + review1.rating) / provider.total_reviews

        # Contrato 2: Completado con reseña
        pintura_service = next(s for s in services if s.title.startswith("Pinta tu casa"))
        contract2 = Contract(
            start_date=datetime.utcnow() - timedelta(days=10),
            status="completado",
            client=clients_dict['Eduardo'],
            provider=providers_dict['Mariam'],
            service=pintura_service
        )
        contracts.append(contract2)
        db.session.add(contract2)
        db.session.commit()
        
        review2 = Review(
            rating=5,
            comment="Un fantástico servicio",
            created_at=datetime.utcnow(),
            contract=contract2,
            author=contract2.client,
            recipient=contract2.provider
        )
        db.session.add(review2)

        # Actualizar rating del proveedor
        provider = contract2.provider
        provider.total_reviews += 1
        provider.average_rating = ((provider.average_rating * (provider.total_reviews - 1)) + review2.rating) / provider.total_reviews

        # Contratos aleatorios
        for _ in range(20):
            client = random.choice(clients)
            service = random.choice(services)
            if client.id == service.provider_id:
                continue

            contract = Contract(
                start_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                status=random.choice(["esperando confirmación", "confirmado", "cancelado"]),
                client=client,
                provider=service.provider,
                service=service
            )
            contracts.append(contract)
            db.session.add(contract)

        db.session.commit()
        print(f"✔️ {len(contracts)} contratos y reseñas creadas.")
        print("🎉 ¡Base de datos poblada con éxito!")

if __name__ == '__main__':
    seed_database()