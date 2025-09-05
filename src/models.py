from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, DateTime, Float
from datetime import datetime
from typing import List
#from enum import Enum as PyEnum


# Inicializamos la extensión de SQLAlchemy
db = SQLAlchemy()
 # 1 ====TABLA QUE GUARDA EL ROL DEL USUARIO
#class UserRole(PyEnum):
 #   CLIENTE = "cliente"
 #   PROVEEDOR = "proveedor"


 
 # 1.1 ====TABLA USER
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=True)
    email: Mapped[str] = mapped_column(String(120), nullable=True) ###preguntar si es opcional entre varios campos, (entonces nullableTrue) o si no es opcional y son obligatorios los dos campos, (nullableFalse)
    phone: Mapped[str] = mapped_column(String(20), nullable=True) ####opcion de registro con telefono agregada
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    average_rating: Mapped[float] = mapped_column(db.Float, default=0.0, nullable=True)
    total_reviews: Mapped[int] = mapped_column(db.Integer, default=0, nullable=True)

    services: Mapped[List["Service"]] = relationship(back_populates="provider")
    contracts_as_client: Mapped[list["Contract"]] = relationship(back_populates="client", foreign_keys="Contract.client_id")
    contracts_as_provider: Mapped[list["Contract"]] = relationship(back_populates="provider", foreign_keys="Contract.provider_id")


    def __repr__(self):
        return f"{self.name} {self.last_name} ({self.role})"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "photo_url": self.photo_url,
            "is_active": self.is_active,
            "average_rating": round(self.average_rating or 0, 2),
            "total_reviews": self.total_reviews
        }


 # 2 ==== TABLA CATEGORIA DEL SERVICIO
class Category(db.Model):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
     #RELATIONSHIPPS
    services: Mapped[List["Service"]] = relationship(back_populates="category")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


 # 3 ====TABLA SERVICIOS
class Service(db.Model):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=True) ###cargar imagen desde una url, barajar la opcion de upload luego

    provider_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    provider: Mapped["User"] = relationship(back_populates="services")
    category: Mapped["Category"] = relationship(back_populates="services")
    contracts: Mapped[list["Contract"]] = relationship(back_populates="service")


    def __repr__(self):
        return f"{self.title} - {self.provider.name} (${self.price})"


    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "photo_url": self.photo_url,
            "provider": self.provider.serialize() if self.provider else None,
            "category": self.category.name if self.category else None,
        }
    
 # 4 ====TABLA CONTRATACIONES(antes booking)
class Contract(db.Model):
    __tablename__ = "contracts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(50), default="esperando confirmación")

    client_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    provider_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)

    client: Mapped["User"] = relationship(back_populates="contracts_as_client", foreign_keys=[client_id])
    provider: Mapped["User"] = relationship(back_populates="contracts_as_provider", foreign_keys=[provider_id])
    service: Mapped["Service"] = relationship(back_populates="contracts")
    reviews: Mapped[list["Review"]] = relationship(back_populates="contract")



    def __repr__(self):
        return f"Contrato #{self.id} - {self.client.name} ↔ {self.provider.name} ({self.status})"

    def serialize(self):
        return {
            "id": self.id,
            "start_date": self.start_date.isoformat(),
            "status": self.status,
            "client": self.client.name if self.client else None,
            "provider": self.provider.name if self.provider else None,
            "service": self.service.title if self.service else None,
        }



 # 5 ====TABLA RESEÑAS
class Review(db.Model):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 estrellas
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    contract: Mapped["Contract"] = relationship(back_populates="reviews")
    author: Mapped["User"] = relationship(foreign_keys=[author_id])
    recipient: Mapped["User"] = relationship(foreign_keys=[recipient_id])




    def __repr__(self):
        return f"Reseña #{self.id} - {self.author.name} → {self.recipient.name} ({'⭐' * self.rating})" #prueba de multiplicar las estrellas para que se vea la calificacion total

    def serialize(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat(),
            "author": self.author.name if self.author else None,
            "recipient_id": self.recipient_id
        }

    @validates("rating")
    def validate_rating(self, key, value):
        value = int(value)
        if value < 1 or value > 5:
            raise ValueError("El rating debe estar entre 1 y 5")
        return value



####emoji de wpp:⭐########






