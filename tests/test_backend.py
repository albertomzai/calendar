import datetime
import json

import pytest

from backend import app, db, Evento

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        with app.app_context():
            # Preparar la base de datos en memoria para pruebas
            db.drop_all()
            db.create_all()
        yield client

def test_get_events_empty(test_client):
    response = test_client.get('/api/events')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list) and len(data) == 0

def test_create_event(test_client):
    payload = {
        'titulo': 'Prueba',
        'fecha_inicio': datetime.datetime.now().isoformat(),
        'fecha_fin': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()
    }
    response = test_client.post('/api/events', json=payload)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['titulo'] == 'Prueba'

def test_get_events_with_data(test_client):
    response = test_client.get('/api/events')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 1

def test_update_event(test_client):
    # Obtener el ID del evento creado anteriormente
    event_id = Evento.query.first().id
    new_title = 'Actualizado'
    payload = {'titulo': new_title}
    response = test_client.put(f'/api/events/{event_id}', json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['titulo'] == new_title

def test_delete_event(test_client):
    event_id = Evento.query.first().id
    response = test_client.delete(f'/api/events/{event_id}')
    assert response.status_code == 204
    # Verificar que el evento ya no existe
    response = test_client.get('/api/events')
    data = json.loads(response.data)
    assert len(data) == 0