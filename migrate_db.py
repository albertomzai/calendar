# Script para crear la base de datos SQLite si no existe.

import os

from backend import db, app

def main():
    with app.app_context():
        if not os.path.exists('calendario.db'):
            db.create_all()
            print('Base de datos creada: calendario.db')
        else:
            print('La base de datos ya existe.')

if __name__ == '__main__':
    main()