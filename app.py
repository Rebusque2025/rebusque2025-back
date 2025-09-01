import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from src.models import db
from src.routes import main # Importa el Blueprint 'main'
from src.routes import search_bp # Importo el blueprint 'search'
from src.admin import setup_admin
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_jwt_extended import JWTManager

# Crea la instancia de la aplicación Flask
app = Flask(__name__, template_folder='src/templates')

load_dotenv()


# Configurar la clave secreta
app.config["JWT_SECRET_KEY"] = "super-secret-key"  

# Inicializar el gestor JWT con la app
jwt = JWTManager(app)

# Configuración de la aplicación
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Inicializa las extensiones con la aplicación
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
# Registra los Blueprints
app.register_blueprint(main)
setup_admin(app)
app.register_blueprint(search_bp)
if __name__ == '__main__':
    with app.app_context():
        # Crea todas las tablas si no existen.
        # Esto es solo para la primera vez, se recomienda usar Flask-Migrate
        db.create_all()
    
    # Inicia el servidor
    app.run(debug=True)