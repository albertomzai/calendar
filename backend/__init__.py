import os

from flask import Flask, Blueprint, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Configuración de la base de datos SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'calendario.db')

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instancia de SQLAlchemy
db = SQLAlchemy(app)

# Importar modelos para que se registren con SQLAlchemy
from . import models  # noqa: E402,F401

# Registrar blueprint de la API
from .routes import api_bp  # noqa: E402,F401
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def serve_index():
    """Sirve el archivo index.html del frontend."""
    return send_from_directory(app.static_folder, 'index.html')