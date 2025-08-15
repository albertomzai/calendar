# backend/routes.py

from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from .models import Evento
from . import db

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET'])
def get_events():
    """Return all events, optionally filtered by start and end datetime."""
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    query = Evento.query

    try:
        if start_str:
            start_dt = datetime.fromisoformat(start_str)
            query = query.filter(Evento.fecha_inicio >= start_dt)
        if end_str:
            end_dt = datetime.fromisoformat(end_str)
            query = query.filter(Evento.fecha_fin <= end_dt)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601.'}), 400

    events = query.all()
    return jsonify([e.to_dict() for e in events])

@events_bp.route('/events', methods=['POST'])
def create_event():
    """Create a new event. Requires titulo, fecha_inicio, and fecha_fin."""
    data = request.get_json() or {}

    required_fields = ['titulo', 'fecha_inicio', 'fecha_fin']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields.'}), 400

    try:
        fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
        fecha_fin = datetime.fromisoformat(data['fecha_fin'])
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601.'}), 400

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

@events_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an existing event. Accepts any of the updatable fields."""
    evento = Evento.query.get_or_404(event_id)

    data = request.get_json() or {}

    if 'titulo' in data:
        evento.titulo = data['titulo']

    if 'descripcion' in data:
        evento.descripcion = data['descripcion']

    if 'fecha_inicio' in data:
        try:
            evento.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
        except ValueError:
            return jsonify({'error': 'Invalid fecha_inicio format.'}), 400

    if 'fecha_fin' in data:
        try:
            evento.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
        except ValueError:
            return jsonify({'error': 'Invalid fecha_fin format.'}), 400

    if 'color' in data:
        evento.color = data['color']

    db.session.commit()
    return jsonify(evento.to_dict())

@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event by its ID."""
    evento = Evento.query.get_or_404(event_id)
    db.session.delete(evento)
    db.session.commit()
    return '', 204