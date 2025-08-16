from flask import Blueprint, request, jsonify, abort
from datetime import datetime

from .models import Evento
from . import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/events', methods=['GET'])
def get_events():
    """Devuelve la lista de eventos, opcionalmente filtrada por rango."""
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    query = Evento.query

    if start_str:
        try:
            start_dt = datetime.fromisoformat(start_str)
        except ValueError:
            abort(400, description='Formato de fecha inicio inválido')
        query = query.filter(Evento.fecha_inicio >= start_dt)

    if end_str:
        try:
            end_dt = datetime.fromisoformat(end_str)
        except ValueError:
            abort(400, description='Formato de fecha fin inválido')
        query = query.filter(Evento.fecha_fin <= end_dt)

    eventos = query.all()
    return jsonify([e.to_dict() for e in eventos])

@api_bp.route('/events', methods=['POST'])
def create_event():
    """Crea un nuevo evento a partir de JSON."""
    data = request.get_json() or {}

    titulo = data.get('titulo')
    fecha_inicio_str = data.get('fecha_inicio')
    fecha_fin_str = data.get('fecha_fin')

    if not all([titulo, fecha_inicio_str, fecha_fin_str]):
        abort(400, description='Campos obligatorios faltantes')

    try:
        fecha_inicio = datetime.fromisoformat(fecha_inicio_str)
        fecha_fin = datetime.fromisoformat(fecha_fin_str)
    except ValueError:
        abort(400, description='Formato de fechas inválido')

    evento = Evento(titulo=titulo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, descripcion=data.get('descripcion'), color=data.get('color'))
    db.session.add(evento)
    db.session.commit()

    return jsonify(evento.to_dict()), 201

@api_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Actualiza un evento existente."""
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
            abort(400, description='Formato de fecha inicio inválido')
    if 'fecha_fin' in data:
        try:
            evento.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
        except ValueError:
            abort(400, description='Formato de fecha fin inválido')
    if 'color' in data:
        evento.color = data['color']

    db.session.commit()
    return jsonify(evento.to_dict())

@api_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Elimina un evento."""
    evento = Evento.query.get_or_404(event_id)
    db.session.delete(evento)
    db.session.commit()
    return '', 204