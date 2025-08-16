import json

import pytest

from backend import create_app, db, Evento

@pytest.fixture(scope='module')
def client():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    # Teardown
    with app.app_context():
        db.drop_all()

def test_root_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_event(client):
    payload = {
        'titulo': 'Reunión',
        'descripcion': 'Discusión de proyecto',
        'fecha_inicio': '2024-09-01T10:00:00',
        'fecha_fin': '2024-09-01T11:00:00',
        'color': '#ff0000'
    }
    response = client.post('/api/events', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == payload['titulo']

def test_get_events(client):
    # Asumimos que el evento creado en el test anterior existe
    response = client.get('/api/events')
    assert response.status_code == 200
    events = response.get_json()
    assert isinstance(events, list)
    assert len(events) >= 1

def test_update_event(client):
    # Obtener ID del primer evento
    events = client.get('/api/events').get_json()
    event_id = events[0]['id']

    payload = {'titulo': 'Reunión Actualizada'}
    response = client.put(f'/api/events/{event_id}', json=payload)
    assert response.status_code == 200
    updated = response.get_json()
    assert updated['titulo'] == payload['titulo']

def test_delete_event(client):
    # Obtener ID del primer evento
    events = client.get('/api/events').get_json()
    event_id = events[0]['id']

    response = client.delete(f'/api/events/{event_id}')
    assert response.status_code == 204

    # Confirmar que ya no existe
    get_resp = client.get(f'/api/events/{event_id}')
    assert get_resp.status_code == 404