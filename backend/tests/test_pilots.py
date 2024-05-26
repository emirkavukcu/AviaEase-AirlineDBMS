import pytest
from app import create_app, db
from models import Pilot, User, AircraftType
from config import TestConfig
import bcrypt
import os
import dotenv

dotenv.load_dotenv()

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
    # Populate with test users and pilot data
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user = User(email='test@example.com', password=hashed_password, name='Test User')
    db.session.add(test_user)

    aircraft_type = AircraftType(
        type_id=1,
        name="Boeing 737",
        seat_count=138,
        crew_limit=16,
        passenger_limit=122,
        standard_menu=["Chicken", "Vegetarian"]
    )

    pilot1 = Pilot(
        name='John Doe',
        age=45,
        gender='Male',
        nationality='American',
        known_languages=['English', 'Spanish'],
        vehicle_type_id=1,
        allowed_range=8000,
        seniority_level='senior',
        scheduled_flights=[]
    )
    pilot2 = Pilot(
        name='Jane Smith',
        age=30,
        gender='Female',
        nationality='British',
        known_languages=['English', 'French'],
        vehicle_type_id=1,
        allowed_range=5000,
        seniority_level='junior',
        scheduled_flights=[]
    )
    db.session.add(aircraft_type)
    db.session.add(pilot1)
    db.session.add(pilot2)
    db.session.commit()

@pytest.fixture(scope='function')
def auth_headers(client):
    login_response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    login_data = login_response.get_json()
    if not login_data or 'access_token' not in login_data:
        raise ValueError(f"Failed to obtain access token: {login_response.get_json()}")

    access_token = login_data['access_token']
    return {
        'Authorization': f'Bearer {access_token}'
    }

def test_get_pilots(client, init_database, auth_headers):
    response = client.get('/api/pilots', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert 'pilots' in data
    assert 'total' in data
    assert data['total'] > 0

def test_get_pilots_with_pagination(client, init_database, auth_headers):
    response = client.get('/api/pilots?page=1&per_page=1', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['pilots']) == 1

def test_get_pilots_with_name_filter(client, init_database, auth_headers):
    response = client.get('/api/pilots?name=John', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['name'] == 'John Doe'

def test_get_pilots_with_age_filter(client, init_database, auth_headers):
    response = client.get('/api/pilots?min_age=40', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['name'] == 'John Doe'

def test_get_pilots_with_gender_filter(client, init_database, auth_headers):
    response = client.get('/api/pilots?gender=Female', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['name'] == 'Jane Smith'

def test_get_pilots_with_nationality_filter(client, init_database, auth_headers):
    response = client.get('/api/pilots?nationality=American', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['name'] == 'John Doe'

def test_get_pilots_with_allowed_range_filter(client, init_database, auth_headers):
    response = client.get('/api/pilots?min_allowed_range=6000', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['allowed_range'] == 8000

def test_get_pilots_with_seniority_level_filter(client, init_database, auth_headers):
    response = client.get('/api/pilots?seniority_level=senior', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['seniority_level'] == 'senior'

def test_create_pilot_missing_fields(client, init_database, auth_headers):
    response = client.post('/api/create_pilot', headers=auth_headers, json={})
    data = response.get_json()
    assert response.status_code == 400
    assert 'Missing required fields' in data['error']

def test_create_pilot_success(client, init_database, auth_headers):
    response = client.post('/api/create_pilot', headers=auth_headers, json={
        'name': 'Alice Wonderland',
        'age': 28,
        'gender': 'Female',
        'nationality': 'Canadian',
        'known_languages': ['English', 'French'],
        'vehicle_type_id': 1,
        'allowed_range': 5000,
        'seniority_level': 'junior'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'Pilot created successfully'
    assert data['pilot']['name'] == 'Alice Wonderland'

def test_create_pilot_invalid_data(client, init_database, auth_headers):
    response = client.post('/api/create_pilot', headers=auth_headers, json={
        'name': 'Alice Wonderland',
        'age': 28,
        'gender': 'Female',
        'nationality': 'Canadian',
        'known_languages': 'English, French',  # Invalid type, should be a list
        'vehicle_type_id': 1,
        'allowed_range': 5000,
        'seniority_level': 'junior'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert 'known_languages must be an array of strings' in data['error']

def test_create_pilot_invalid_vehicle_type(client, init_database, auth_headers):
    response = client.post('/api/create_pilot', headers=auth_headers, json={
        'name': 'Alice Wonderland',
        'age': 28,
        'gender': 'Female',
        'nationality': 'Canadian',
        'known_languages': ['English', 'French'],
        'vehicle_type_id': 10,  # Invalid vehicle type
        'allowed_range': 5000,
        'seniority_level': 'junior'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert 'vehicle_type_id must be an integer and one of [1, 2, 3]' in data['error']
