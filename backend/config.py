import os

# Configuración de la base de datos SQLite
class Config:
    """Configuración básica del proyecto."""

    # Ruta relativa al directorio raíz del proyecto
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'calendario.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False