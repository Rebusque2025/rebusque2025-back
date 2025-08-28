from flask_admin.contrib.sqla import ModelView
from wtforms_sqlalchemy.fields import QuerySelectField
from src.models import db, User, Category, Service, Contract, Review
from wtforms import SelectField


# admin de servicios:
class ServiceAdmin(ModelView):
    form_columns = ["title", "description", "price", "provider", "category"]
    form_overrides = {
        "provider": QuerySelectField,
        "category": QuerySelectField,
    }
    form_args = {
        "provider": dict(
            query_factory=lambda: User.query.filter_by(role=User.role).all(),
            get_label="name"
        ),
        "category": dict(
            query_factory=lambda: db.session.query(Category).all(),
            get_label="name"
        ),
    }

class ContractAdmin(ModelView):
    form_overrides ={
        "client": QuerySelectField,
        "provider": QuerySelectField,
        "service": QuerySelectField,
    }
    form_args = {
        "client": dict(
            query_factory=lambda: User.query.filter_by(role=UserRole.CLIENTE).all(),
            get_label="name" 
        ),
        "provider": dict (
            query_factory=lambda: User.query.filter_by(role=UserRole.PROVEEDOR).all(),
            get_label="name" 
        ),
        "service": dict(
            query_factory=lambda: Service.query.all(),
            get_label="title"
        ),
    }


class ReviewAdmin(ModelView):
    form_overrides = {
        "contract": QuerySelectField,
        "author": QuerySelectField,
        "recipient": QuerySelectField,
        "rating": SelectField,
    }

    form_args = {
        "contract": dict (
            query_factory=lambda: Contract.query.all(),
            get_label=lambda item: f"Contrato {item.id} {item.client.name} - {item.provider.name} ({item.status})"
        ),
        "author": dict(
            query_factory=lambda: User.query.all(),
            get_label="name"
        ),
        "recipient": dict(
            query_factory=lambda: User.query.all(),
            get_label="name"
        ),
        "rating": dict(
            choices=[(1, "⭐1"), (2, "⭐2"), (3, "⭐3"), (4, "⭐4"), (5, "⭐5")]
        ),
    }

    #validacion para no dejar reseñas si no esta el estado"completado"
    def on_model_change(self, form, model, is_created):
        if model.contract.status != "completado":
            raise ValueError("Solo se pueden dejar reseñas para contratos completados.")