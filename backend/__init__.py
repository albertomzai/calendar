from flask import Flask

# Importamos las configuraciones de la base de datos
from .config import Config

# Creamos la instancia de Flask con la carpeta estática adecuada
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Cargamos la configuración desde el objeto Config
app.config.from_object(Config)

# Inicializamos SQLAlchemy y creamos los modelos
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# Registramos los Blueprints
from .routes import events_bp
app.register_blueprint(events_bp, url_prefix='/api')

# Ruta raíz para servir el index.html del frontend
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')