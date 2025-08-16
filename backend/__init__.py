import os

from flask import Flask, abort, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Global database instance
db = SQLAlchemy()

def create_app(testing: bool = False) -> Flask:
    """Factory that creates and configures the Flask application.

    Parameters
    ----------
    testing : bool, optional
        If True, the application is configured for unit tests using an in‑memory
        SQLite database. Default is False.

    Returns
    -------
    flask.Flask
        The configured Flask application instance.
    """

    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configure the database URI
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, '..', 'calendario.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise extensions
    db.init_app(app)

# Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

# Root route to serve the frontend index.html
    @app.route('/')
    def root():
        return send_from_directory(app.static_folder, 'index.html')

    # Error handlers for common HTTP errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': error.description}), 400

    return app