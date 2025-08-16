from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializar la extensión de base de datos
db = SQLAlchemy()

# Importar el blueprint de la API
from .routes import api_bp

def create_app():
    """Factory que crea y configura la aplicación Flask."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)

    # Registrar el blueprint de la API
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

# Importar el modelo Evento después de la configuración para evitar ciclos de importación
from .models import Evento

__all__ = ['create_app', 'db', 'Evento']