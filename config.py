# Configuración de la aplicación Flask y SQLAlchemy.
# Se utiliza una base de datos SQLite local llamada "calendario.db".

class Config:
    """Configuración global para la app Flask."""
    SECRET_KEY = 'dev-key'  # No crítico, solo para sesiones de Flask
    SQLALCHEMY_DATABASE_URI = 'sqlite:///calendario.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
