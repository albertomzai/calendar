import os
import json
from datetime import datetime, timedelta

import pytest

from backend import create_app, db
from backend.models import Evento

@pytest.fixture(scope='module')
def test_client():
    # Configurar la app para usar una base de datos en memoria durante las pruebas
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    app = create_app()
    with app.app_context():
        db.create_all()

    client = app.test_client()
    yield client

    # Limpieza: drop tables después de las pruebas
    with app.app_context():
        db.drop_all()

def test_create_event(test_client):
    payload = {
        'titulo': 'Prueba',
        'fecha_inicio': datetime.utcnow().isoformat(),
        'fecha_fin': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }

    response = test_client.post('/api/events', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] is not None
    assert data['titulo'] == 'Prueba'

def test_get_events(test_client):
    # Crear dos eventos para probar el filtro
    now = datetime.utcnow()
    e1 = Evento(titulo='E1', fecha_inicio=now, fecha_fin=now + timedelta(hours=2))
    e2 = Evento(titulo='E2', fecha_inicio=now + timedelta(days=1), fecha_fin=now + timedelta(days=1, hours=2))
    db.session.add_all([e1, e2])
    db.session.commit()

    # Obtener todos los eventos
    response = test_client.get('/api/events')
    assert response.status_code == 200
    events = response.get_json()
    assert len(events) >= 2

    # Filtrar por rango de fechas (solo e1)
    start = now.isoformat()
    end = (now + timedelta(hours=3)).isoformat()
    response = test_client.get(f'/api/events?start={start}&end={end}')
    assert response.status_code == 200
    filtered = response.get_json()
    assert len(filtered) == 1

def test_update_event(test_client):
    # Crear un evento
    event = Evento(titulo='Old', fecha_inicio=datetime.utcnow(), fecha_fin=datetime.utcnow()+timedelta(hours=1))
    db.session.add(event)
    db.session.commit()

    payload = { 'titulo': 'New', 'color': '#FF0000' }
    response = test_client.put(f'/api/events/{event.id}', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'New'
    assert data['color'] == '#FF0000'

def test_delete_event(test_client):
    event = Evento(titulo='ToDelete', fecha_inicio=datetime.utcnow(), fecha_fin=datetime.utcnow()+timedelta(hours=1))
    db.session.add(event)
    db.session.commit()

    response = test_client.delete(f'/api/events/{event.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Evento eliminado'

    # Verificar que ya no existe en la BD
    with test_client.application.app_context():
        assert Evento.query.get(event.id) is None