# tests/test_backend.py

import pytest
from backend import app as flask_app, db

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        # Setup in-memory database for tests
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_get_events_empty(client):
    response = client.get('/api/events')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_event(client):
    payload = {
        'titulo': 'Reunión',
        'fecha_inicio': '2025-08-15T10:00:00',
        'fecha_fin': '2025-08-15T11:00:00',
        'descripcion': 'Discusión de proyecto',
        'color': '#ff0000'
    }
    response = client.post('/api/events', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == payload['titulo']

def test_get_events_with_data(client):
    # Create an event first
    client.post('/api/events', json={
        'titulo': 'Evento 1',
        'fecha_inicio': '2025-08-10T09:00:00',
        'fecha_fin': '2025-08-10T10:00:00'
    })
    response = client.get('/api/events')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1

def test_update_event(client):
    # Create event
    post_resp = client.post('/api/events', json={
        'titulo': 'Old Title',
        'fecha_inicio': '2025-08-20T12:00:00',
        'fecha_fin': '2025-08-20T13:00:00'
    })
    event_id = post_resp.get_json()['id']

    # Update title
    put_resp = client.put(f'/api/events/{event_id}', json={'titulo': 'New Title'})
    assert put_resp.status_code == 200
    updated = put_resp.get_json()
    assert updated['titulo'] == 'New Title'

def test_delete_event(client):
    # Create event
    post_resp = client.post('/api/events', json={
        'titulo': 'To Delete',
        'fecha_inicio': '2025-08-25T14:00:00',
        'fecha_fin': '2025-08-25T15:00:00'
    })
    event_id = post_resp.get_json()['id']

    del_resp = client.delete(f'/api/events/{event_id}')
    assert del_resp.status_code == 204

    # Ensure it's gone
    get_resp = client.get('/api/events')
    data = get_resp.get_json()
    assert len(data) == 0