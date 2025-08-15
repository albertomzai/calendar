# backend/app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)

db = SQLAlchemy(app)

# Registrar blueprint después de que db esté definido
from .routes import events_bp
app.register_blueprint(events_bp, url_prefix='/api')

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')