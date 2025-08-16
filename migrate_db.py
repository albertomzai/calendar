# Script para crear la base de datos SQLite si no existe.

from backend import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print('Base de datos creada o ya existía.')