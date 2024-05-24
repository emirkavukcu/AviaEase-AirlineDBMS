import pytest
from app import create_app, db
from models import Passenger
from config import TestConfig

@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.create_all()
        populate_db()
        yield db
        db.session.remove()
        db.drop_all()

def populate_db():
    passenger1 = Passenger(
        passenger_id=1,
        name='John Doe',
        age=30,
        gender='Male',
        nationality='American',
        parent_id=None,
        affiliated_passenger_ids=[],
        scheduled_flights=[]
    )
    passenger2 = Passenger(
        passenger_id=2,
        name='Jane Smith',
        age=25,
        gender='Female',
        nationality='British',
        parent_id=None,
        affiliated_passenger_ids=[],
        scheduled_flights=[]
    )
    db.session.add(passenger1)
    db.session.add(passenger2)
    db.session.commit()

def test_get_passengers(client, init_database):
    response = client.get('/passengers')
    data = response.get_json()
    assert response.status_code == 200
    assert data['total'] == 2
    assert any(p['name'] == 'John Doe' for p in data['passengers'])
    assert any(p['name'] == 'Jane Smith' for p in data['passengers'])

def test_get_passengers_with_pagination(client, init_database):
    response = client.get('/passengers?page=1&per_page=1')
    data = response.get_json()
    assert response.status_code == 200
    assert data['total'] == 2
    assert len(data['passengers']) == 1

def test_get_passengers_with_name_filter(client, init_database):
    response = client.get('/passengers?name=John')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'John Doe'

def test_get_passengers_with_age_filter(client, init_database):
    response = client.get('/passengers?min_age=26')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'John Doe'

def test_get_passengers_with_gender_filter(client, init_database):
    response = client.get('/passengers?gender=Female')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'Jane Smith'

def test_get_passengers_with_nationality_filter(client, init_database):
    response = client.get('/passengers?nationality=British')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'Jane Smith'

def test_create_passenger_missing_fields(client):
    response = client.post('/create_passenger', json={})
    data = response.get_json()
    assert response.status_code == 400
    assert 'Missing required data' in data['error']

def test_create_passenger_success(client):
    response = client.post('/create_passenger', json={
        'name': 'Alice Wonderland',
        'age': 28,
        'gender': 'Female',
        'nationality': 'Canadian'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'Passenger created successfully'
    assert data['passenger']['name'] == 'Alice Wonderland'

def test_create_passenger_duplicate(client, init_database):
    response = client.post('/create_passenger', json={
        'name': 'John Doe',
        'age': 30,
        'gender': 'Male',
        'nationality': 'American'
    })
    assert response.status_code == 500

def test_create_passenger_invalid_data(client):
    response = client.post('/create_passenger', json={
        'name': '',
        'age': -1,
        'gender': 'Unknown',
        'nationality': ''
    })
    assert response.status_code == 400
    assert 'Missing required data' in response.get_json()['error']
