import pytest
from datetime import datetime, timedelta

from backend import create_app, db
from backend.models import Event

@pytest.fixture(scope='module')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_event(client):
    payload = {
        'titulo': 'Reunión',
        'fecha_inicio': datetime.utcnow().isoformat(),
        'fecha_fin': (datetime.utcnow() + timedelta(hours=1)).isoformat()
    }
    resp = client.post('/api/events', json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['titulo'] == 'Reunión'

def test_get_events(client):
    # Create two events in memory
    from datetime import datetime, timedelta
    start1 = datetime.utcnow()
    end1 = start1 + timedelta(hours=2)

    event1 = Event(titulo='Evento 1', fecha_inicio=start1, fecha_fin=end1)
    db.session.add(event1)
    db.session.commit()

    resp = client.get('/api/events')
    assert resp.status_code == 200
    events = resp.get_json()
    assert any(e['id'] == event1.id for e in events)

def test_update_event(client):
    # Create an event
    from datetime import datetime, timedelta
    start = datetime.utcnow()
    end = start + timedelta(hours=2)
    event = Event(titulo='Old', fecha_inicio=start, fecha_fin=end)
    db.session.add(event)
    db.session.commit()

    payload = {'titulo': 'New Title'}
    resp = client.put(f'/api/events/{event.id}', json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['titulo'] == 'New Title'

def test_delete_event(client):
    # Create an event
    from datetime import datetime, timedelta
    start = datetime.utcnow()
    end = start + timedelta(hours=2)
    event = Event(titulo='ToDelete', fecha_inicio=start, fecha_fin=end)
    db.session.add(event)
    db.session.commit()

    resp = client.delete(f'/api/events/{event.id}')
    assert resp.status_code == 200
    # Verify deletion
    get_resp = client.get('/api/events')
    events = get_resp.get_json()
    assert all(e['id'] != event.id for e in events)