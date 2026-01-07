from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.models import db, User, Category, Service, Contract, Review
from src.admin_config import ServiceAdmin, ContractAdmin, ReviewAdmin


def setup_admin(app):
    admin = Admin(app, name='Rebusque2025')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Category, db.session))

    admin.add_view(ServiceAdmin(Service, db.session))
    admin.add_view(ContractAdmin(Contract, db.session))
    admin.add_view(ReviewAdmin(Review, db.session))
    return admin







