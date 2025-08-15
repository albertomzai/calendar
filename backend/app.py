# Script de arranque del servidor Flask

from . import app, db

if __name__ == '__main__':
    # Creamos la base de datos si no existe
    with app.app_context():
        db.create_all()

    # Iniciamos el servidor
    app.run(host='0.0.0.0', port=5000, debug=True)