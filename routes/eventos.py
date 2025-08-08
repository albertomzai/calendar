# Rutas de la API para eventos.
# Se implementan los endpoints GET, POST, PUT y DELETE según el contrato.

from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from app import sql
from models.evento import Evento

events_bp = Blueprint('events', __name__)

@events_bp.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad Request', 'message': str(e)}), 400

@events_bp.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not Found', 'message': str(e)}), 404

@events_bp.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

# ---------- GET /api/events ----------
@events_bp.route('', methods=['GET'])
def get_events():
    """Devuelve todos los eventos dentro de un rango de fechas.

    Parámetros opcionales:
        start: ISO8601 datetime string (inclusive)
        end:   ISO8601 datetime string (exclusive)
    """
    try:
        start_str = request.args.get('start')
        end_str = request.args.get('end')
        query = Evento.query
        if start_str:
            start_dt = datetime.fromisoformat(start_str)
            query = query.filter(Evento.fecha_inicio >= start_dt)
        if end_str:
            end_dt = datetime.fromisoformat(end_str)
            query = query.filter(Evento.fecha_fin <= end_dt)
        eventos = [e.to_dict() for e in query.all()]
        return jsonify(eventos), 200
    except Exception as exc:
        abort(400, description=str(exc))

# ---------- POST /api/events ----------
@events_bp.route('', methods=['POST'])
def create_event():
    """Crea un nuevo evento.

    Espera JSON con: titulo, descripcion, fecha_inicio, fecha_fin, color.
    """
    data = request.get_json(force=True)
    required_fields = ['titulo', 'fecha_inicio', 'fecha_fin']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')
    try:
        evento = Evento(
            titulo=data['titulo'],
            descripcion=data.get('descripcion', ''),
            fecha_inicio=datetime.fromisoformat(data['fecha_inicio']),
            fecha_fin=datetime.fromisoformat(data['fecha_fin']),
            color=data.get('color', '#3788d8')
        )
        sql.session.add(evento)
        sql.session.commit()
        return jsonify(evento.to_dict()), 201
    except Exception as exc:
        sql.session.rollback()
        abort(400, description=str(exc))

# ---------- PUT /api/events/<id> ----------
@events_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Actualiza un evento existente."""
    data = request.get_json(force=True)
    evento = Evento.query.get_or_404(event_id, description='Event not found')
    try:
        if 'titulo' in data:
            evento.titulo = data['titulo']
        if 'descripcion' in data:
            evento.descripcion = data['descripcion']
        if 'fecha_inicio' in data:
            evento.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
        if 'fecha_fin' in data:
            evento.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
        if 'color' in data:
            evento.color = data['color']
        sql.session.commit()
        return jsonify(evento.to_dict()), 200
    except Exception as exc:
        sql.session.rollback()
        abort(400, description=str(exc))

# ---------- DELETE /api/events/<id> ----------
@events_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Elimina un evento."""
    evento = Evento.query.get_or_404(event_id, description='Event not found')
    try:
        sql.session.delete(evento)
        sql.session.commit()
        return jsonify({'message': 'Deleted', 'deleted_id': event_id}), 200
    except Exception as exc:
        sql.session.rollback()
        abort(500, description=str(exc))
