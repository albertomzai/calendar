#!/usr/bin/env python3
"""Entrypoint del servidor Flask.

Este archivo expone tanto la API RESTful para gestionar eventos como el contenido estático de la SPA.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from app import create_app

# Inicializamos la aplicación a través de la fábrica
app = create_app()
CORS(app)  # Permite peticiones desde localhost:3000 (frontend)

@app.route('/')
def index():
    """Sirve el archivo index.html del frontend.

    Se espera que el directorio ``static`` contenga la SPA generada por el cliente.
    """
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
