from flask import Flask, Blueprint, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

# Instancia de la extensión SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Factory que crea y configura la aplicación Flask."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)

    # Registrar blueprints
    from .routes import events_bp
    app.register_blueprint(events_bp, url_prefix='/api')

    # Ruta raíz para servir el index.html del frontend
    @app.route('/')
    def serve_root():
        return app.send_static_file('index.html')

    # Manejo de errores con respuestas JSON
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso no encontrado'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Solicitud inválida'}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500

    return app