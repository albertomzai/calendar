# Pruebas unitarias para la API de eventos.
# Se usa el test_client de Flask y pytest.

import json
from datetime import datetime, timedelta
import pytest
from backend import app as flask_app
from app import sql
from models.evento import Evento

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Utilidad para crear un evento de prueba

def create_event(client, titulo='Test', descripcion='', color='#123456'):
    now = datetime.utcnow()
    payload = {
        'titulo': titulo,
        'descripcion': descripcion,
        'fecha_inicio': (now + timedelta(days=1)).isoformat(),
        'fecha_fin': (now + timedelta(days=2)).isoformat(),
        'color': color
    }
    resp = client.post('/api/events', data=json.dumps(payload), content_type='application/json')
    return json.loads(resp.data)

# ---------- Test GET ----------

def test_get_events_empty(client):
    resp = client.get('/api/events')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)

# ---------- Test POST ----------

def test_create_event_success(client):
    new_evt = create_event(client)
    assert 'id' in new_evt
    assert new_evt['titulo'] == 'Test'

# ---------- Test PUT ----------

def test_update_event_success(client):
    evt = create_event(client)
    update_payload = {'titulo': 'Updated', 'color': '#abcdef'}
    resp = client.put(f"/api/events/{evt['id']}", data=json.dumps(update_payload), content_type='application/json')
    assert resp.status_code == 200
    updated = json.loads(resp.data)
    assert updated['titulo'] == 'Updated'
    assert updated['color'] == '#abcdef'

# ---------- Test DELETE ----------

def test_delete_event_success(client):
    evt = create_event(client)
    resp = client.delete(f"/api/events/{evt['id']}")
    assert resp.status_code == 200
    msg = json.loads(resp.data)
    assert msg['deleted_id'] == evt['id']
