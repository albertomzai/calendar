# backend/__init__.py

# Expose the Flask app and SQLAlchemy db as top-level imports.
from .app import app  # Importa la instancia de Flask creada en app.py
from .models import Evento  # Importa el modelo para que esté disponible
from flask_sqlalchemy import SQLAlchemy

# Reexport db from backend/app.py to keep API stable
from .app import db
__all__ = ['app', 'db', 'Evento']