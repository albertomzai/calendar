# Inicialización del paquete "app"
# Se crea la instancia de Flask y se registra el Blueprint de eventos.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Instancia global de SQLAlchemy que será usada por los modelos
sql = SQLAlchemy()

def create_app():
    """Factory para crear la aplicación Flask.

    Se registra el Blueprint de eventos y se crean las tablas en la BD.
    """
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    sql.init_app(app)

    from .routes.eventos import events_bp
    app.register_blueprint(events_bp, url_prefix='/api/events')

    # Crear tablas al iniciar la aplicación (solo en dev; en prod usar migraciones)
    with app.app_context():
        sql.create_all()

    return app
