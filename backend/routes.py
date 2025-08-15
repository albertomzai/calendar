from flask import Blueprint, request, jsonify, abort
from datetime import datetime

from .models import Evento
from . import db

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET'])
def get_events():
    """Devuelve todos los eventos filtrados por rango de fechas."""
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    query = Evento.query

    if start_str:
        try:
            start_date = datetime.fromisoformat(start_str)
        except ValueError:
            abort(400, description='Formato de fecha inicio inválido')
        query = query.filter(Evento.fecha_inicio >= start_date)

    if end_str:
        try:
            end_date = datetime.fromisoformat(end_str)
        except ValueError:
            abort(400, description='Formato de fecha fin inválido')
        query = query.filter(Evento.fecha_fin <= end_date)

    eventos = query.all()
    return jsonify([e.to_dict() for e in eventos])

@events_bp.route('/events', methods=['POST'])
def create_event():
    """Crea un nuevo evento a partir de los datos JSON enviados."""
    data = request.get_json() or {}

    titulo = data.get('titulo')
    fecha_inicio_str = data.get('fecha_inicio')
    fecha_fin_str = data.get('fecha_fin')

    if not all([titulo, fecha_inicio_str, fecha_fin_str]):
        abort(400, description='Campos requeridos: titulo, fecha_inicio, fecha_fin')

    try:
        fecha_inicio = datetime.fromisoformat(fecha_inicio_str)
        fecha_fin = datetime.fromisoformat(fecha_fin_str)
    except ValueError:
        abort(400, description='Formato de fechas inválido')

    evento = Evento(titulo=titulo, descripcion=data.get('descripcion', ''),
                    fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                    color=data.get('color', '#0000ff'))
    db.session.add(evento)
    db.session.commit()

    return jsonify(evento.to_dict()), 201

@events_bp.route('/events/<int:event_id>', methods=['PUT'])
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

@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Elimina un evento existente."""
    evento = Evento.query.get_or_404(event_id)

    db.session.delete(evento)
    db.session.commit()

    return jsonify({'message': 'Evento eliminado'}), 200