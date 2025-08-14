from flask import Blueprint, request, jsonify, abort
from datetime import datetime

from . import db
from .models import Evento

events_bp = Blueprint('events', __name__)

# Helper para parsear fechas ISO8601
def _parse_iso(dt_str):
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        abort(400, description='Formato de fecha inválido')

@events_bp.route('/events', methods=['GET'])
def get_events():
    start = request.args.get('start')
    end = request.args.get('end')

    query = Evento.query
    if start:
        query = query.filter(Evento.fecha_inicio >= _parse_iso(start))
    if end:
        query = query.filter(Evento.fecha_fin <= _parse_iso(end))

    eventos = query.all()
    return jsonify([e.to_dict() for e in eventos]), 200

@events_bp.route('/events', methods=['POST'])
def create_event():
    data = request.get_json() or {}
    titulo = data.get('titulo')
    fecha_inicio_str = data.get('fecha_inicio')
    fecha_fin_str = data.get('fecha_fin')

    if not all([titulo, fecha_inicio_str, fecha_fin_str]):
        abort(400, description='Campos obligatorios: titulo, fecha_inicio, fecha_fin')

    fecha_inicio = _parse_iso(fecha_inicio_str)
    fecha_fin = _parse_iso(fecha_fin_str)

    evento = Evento(titulo=titulo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, descripcion=data.get('descripcion', ''), color=data.get('color', '#FFFFFF'))
    db.session.add(evento)
    db.session.commit()

    return jsonify(evento.to_dict()), 201

@events_bp.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    evento = Evento.query.get_or_404(event_id)
    data = request.get_json() or {}

    if 'titulo' in data:
        evento.titulo = data['titulo']
    if 'descripcion' in data:
        evento.descripcion = data['descripcion']
    if 'fecha_inicio' in data:
        evento.fecha_inicio = _parse_iso(data['fecha_inicio'])
    if 'fecha_fin' in data:
        evento.fecha_fin = _parse_iso(data['fecha_fin'])
    if 'color' in data:
        evento.color = data['color']

    db.session.commit()
    return jsonify(evento.to_dict()), 200

@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    evento = Evento.query.get_or_404(event_id)
    db.session.delete(evento)
    db.session.commit()
    return jsonify({'message': 'Evento eliminado'}), 200