import datetime

from flask import Blueprint, request, jsonify, abort
from .models import Evento
from . import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/events', methods=['GET'])
def get_events():
    """Devuelve todos los eventos, con opción de filtrar por rango."""
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    query = Evento.query

    try:
        if start_str:
            start_dt = datetime.datetime.fromisoformat(start_str)
            query = query.filter(Evento.fecha_inicio >= start_dt)
        if end_str:
            end_dt = datetime.datetime.fromisoformat(end_str)
            query = query.filter(Evento.fecha_fin <= end_dt)
    except ValueError:
        abort(400, description='Fecha inválida')

    eventos = [e.to_dict() for e in query.all()]
    return jsonify(eventos), 200

@api_bp.route('/events', methods=['POST'])
def create_event():
    """Crea un nuevo evento a partir de los datos JSON."""
    data = request.get_json() or {}
    required_fields = ['titulo', 'fecha_inicio', 'fecha_fin']

    if not all(field in data for field in required_fields):
        abort(400, description='Campos obligatorios faltantes')

    try:
        fecha_inicio = datetime.datetime.fromisoformat(data['fecha_inicio'])
        fecha_fin = datetime.datetime.fromisoformat(data['fecha_fin'])
    except ValueError:
        abort(400, description='Formato de fecha inválido')

    evento = Evento(
        titulo=data['titulo'],
        descripcion=data.get('descripcion'),
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        color=data.get('color')
    )

    db.session.add(evento)
    db.session.commit()

    return jsonify(evento.to_dict()), 201

@api_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Actualiza los campos de un evento existente."""
    evento = Evento.query.get_or_404(event_id)
    data = request.get_json() or {}

    if 'titulo' in data:
        evento.titulo = data['titulo']
    if 'descripcion' in data:
        evento.descripcion = data['descripcion']
    if 'fecha_inicio' in data:
        try:
            evento.fecha_inicio = datetime.datetime.fromisoformat(data['fecha_inicio'])
        except ValueError:
            abort(400, description='Formato de fecha inválido')
    if 'fecha_fin' in data:
        try:
            evento.fecha_fin = datetime.datetime.fromisoformat(data['fecha_fin'])
        """Actualiza la fecha de fin."""
        except ValueError:
            abort(400, description='Formato de fecha inválido')

    db.session.commit()
    return jsonify(evento.to_dict()), 200

@api_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Elimina el evento especificado."""
    evento = Evento.query.get_or_404(event_id)
    db.session.delete(evento)
    db.session.commit()
    return '', 204