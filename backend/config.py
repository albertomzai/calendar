# backend/config.py

class Config:
    """Configuration class for the Flask application."""

    # SQLite database file in the project root
    SQLALCHEMY_DATABASE_URI = 'sqlite:///calendario.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False