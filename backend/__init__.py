from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicializar la extensión de SQLAlchemy sin app todavía
db = SQLAlchemy()

def create_app(test_config=None):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración por defecto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is not None:
        app.config.update(test_config)

    # Inicializar la base de datos con la aplicación
    db.init_app(app)

    # Registrar blueprints
    from .events import events_bp
    app.register_blueprint(events_bp, url_prefix='/api/events')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app