from flask import Blueprint, request, jsonify
from datetime import datetime

from .models import Event
from . import db

events_bp = Blueprint('events', __name__)

@events_bp.route('', methods=['GET'])
def get_events():
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    query = Event.query

    if start_str:
        try:
            start_dt = datetime.fromisoformat(start_str)
        except ValueError:
            return jsonify({'error': 'Invalid start date format'}), 400
        query = query.filter(Event.fecha_inicio >= start_dt)

    if end_str:
        try:
            end_dt = datetime.fromisoformat(end_str)
        except ValueError:
            return jsonify({'error': 'Invalid end date format'}), 400
        query = query.filter(Event.fecha_fin <= end_dt)

    events = query.all()
    return jsonify([e.to_dict() for e in events])

@events_bp.route('', methods=['POST'])
def create_event():
    data = request.get_json() or {}
    titulo = data.get('titulo')
    fecha_inicio_str = data.get('fecha_inicio')
    fecha_fin_str = data.get('fecha_fin')

    if not all([titulo, fecha_inicio_str, fecha_fin_str]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        fecha_inicio = datetime.fromisoformat(fecha_inicio_str)
        fecha_fin = datetime.fromisoformat(fecha_fin_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    if fecha_fin < fecha_inicio:
        return jsonify({'error': 'fecha_fin must be after fecha_inicio'}), 400

    event = Event(
        titulo=titulo,
        descripcion=data.get('descripcion'),
        color=data.get('color'),
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    db.session.add(event)
    db.session.commit()

    return jsonify(event.to_dict()), 201

@events_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json() or {}

    if 'titulo' in data:
        event.titulo = data['titulo']

    if 'descripcion' in data:
        event.descripcion = data['descripcion']

    if 'color' in data:
        event.color = data['color']

    if 'fecha_inicio' in data:
        try:
            event.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
        except ValueError:
            return jsonify({'error': 'Invalid fecha_inicio format'}), 400

    if 'fecha_fin' in data:
        try:
            event.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
        except ValueError:
            return jsonify({'error': 'Invalid fecha_fin format'}), 400

    if event.fecha_fin < event.fecha_inicio:
        return jsonify({'error': 'fecha_fin must be after fecha_inicio'}), 400

    db.session.commit()
    return jsonify(event.to_dict())

@events_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200