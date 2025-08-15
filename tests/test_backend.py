import json

from backend import app, db
from backend.models import Evento

import pytest

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        # Creamos la base de datos en memoria para pruebas
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

        yield client

        db.session.remove()
        db.drop_all()

def test_create_event(test_client):
    payload = {
        'titulo': 'Reunión',
        'fecha_inicio': '2025-08-20T10:00:00',
        'fecha_fin': '2025-08-20T11:00:00'
    }

    response = test_client.post('/api/events', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['titulo'] == 'Reunión'

def test_get_events(test_client):
    # Insertamos manualmente un evento
    e = Evento(titulo='Prueba', fecha_inicio=Evento.fecha_inicio, fecha_fin=Evento.fecha_fin)
    db.session.add(e)
    db.session.commit()

    response = test_client.get('/api/events')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_update_event(test_client):
    e = Evento(titulo='Old', fecha_inicio=Evento.fecha_inicio, fecha_fin=Evento.fecha_fin)
    db.session.add(e)
    db.session.commit()

    payload = {'titulo': 'Updated'}
    response = test_client.put(f'/api/events/{e.id}', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200

def test_delete_event(test_client):
    e = Evento(titulo='ToDelete', fecha_inicio=Evento.fecha_inicio, fecha_fin=Evento.fecha_fin)
    db.session.add(e)
    db.session.commit()

    response = test_client.delete(f'/api/events/{e.id}')
    assert response.status_code == 200