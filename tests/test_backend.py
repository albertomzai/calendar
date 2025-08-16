import pytest
from datetime import datetime, timedelta

from backend import create_app, db, Evento

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # Usar una BD en memoria para los tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_db():
    # Garantiza que cada test empieza con DB vacía
    yield
    with db.session.no_autoflush:
        db.session.query(Evento).delete()
        db.session.commit()

def test_create_event(client):
    payload = {
        'titulo': 'Prueba',
        'fecha_inicio': datetime.utcnow().isoformat(),
        'fecha_fin': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }
    resp = client.post('/api/events', json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['titulo'] == 'Prueba'

def test_get_events(client):
    # Crear dos eventos
    e1 = Evento(titulo='A', fecha_inicio=datetime.utcnow(), fecha_fin=datetime.utcnow()+timedelta(hours=2))
    e2 = Evento(titulo='B', fecha_inicio=datetime.utcnow()+timedelta(days=1), fecha_fin=datetime.utcnow()+timedelta(days=1, hours=2))
    db.session.add_all([e1, e2])
    db.session.commit()

    resp = client.get('/api/events')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2

def test_update_event(client):
    evento = Evento(titulo='Old', fecha_inicio=datetime.utcnow(), fecha_fin=datetime.utcnow()+timedelta(hours=1))
    db.session.add(evento)
    db.session.commit()

    new_title = 'Updated'
    resp = client.put(f'/api/events/{evento.id}', json={'titulo': new_title})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['titulo'] == new_title

def test_delete_event(client):
    evento = Evento(titulo='ToDelete', fecha_inicio=datetime.utcnow(), fecha_fin=datetime.utcnow()+timedelta(hours=1))
    db.session.add(evento)
    db.session.commit()

    resp = client.delete(f'/api/events/{evento.id}')
    assert resp.status_code == 204
    # Verificar que ya no existe
    assert Evento.query.get(evento.id) is None