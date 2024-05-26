import pytest
from app import create_app, db
from models import Passenger, User
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
    # Populate with test users and passenger data
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user = User(email='test@example.com', password=hashed_password, name='Test User')
    db.session.add(test_user)
    
    passenger1 = Passenger(
        name='John Doe',
        age=30,
        gender='Male',
        nationality='American',
        parent_id=None,
        affiliated_passenger_ids=[],
        scheduled_flights=[]
    )
    passenger2 = Passenger(
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

@pytest.fixture(scope='function')
def auth_headers(client):
    login_response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    print("Login Response Status Code:", login_response.status_code)
    print("Login Response Data:", login_response.get_json())  # Debugging print

    login_data = login_response.get_json()
    if not login_data or 'access_token' not in login_data:
        raise ValueError(f"Failed to obtain access token: {login_response.get_json()}")

    access_token = login_data['access_token']
    return {
        'Authorization': f'Bearer {access_token}'
    }

def test_get_passengers(client, init_database, auth_headers):
    response = client.get('/api/passengers', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert data['total'] == 2
    assert any(p['name'] == 'John Doe' for p in data['passengers'])
    assert any(p['name'] == 'Jane Smith' for p in data['passengers'])

def test_get_passengers_with_pagination(client, init_database, auth_headers):
    response = client.get('/api/passengers?page=1&per_page=1', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert data['total'] == 2
    assert len(data['passengers']) == 1

def test_get_passengers_with_name_filter(client, init_database, auth_headers):
    response = client.get('/api/passengers?name=John', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'John Doe'

def test_get_passengers_with_age_filter(client, init_database, auth_headers):
    response = client.get('/api/passengers?min_age=26', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'John Doe'

def test_get_passengers_with_gender_filter(client, init_database, auth_headers):
    response = client.get('/api/passengers?gender=Female', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'Jane Smith'

def test_get_passengers_with_nationality_filter(client, init_database, auth_headers):
    response = client.get('/api/passengers?nationality=British', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['passengers']) == 1
    assert data['passengers'][0]['name'] == 'Jane Smith'

def test_create_passenger_missing_fields(client, init_database, auth_headers):
    response = client.post('/api/create_passenger', headers=auth_headers, json={})
    data = response.get_json()
    assert response.status_code == 400
    assert 'Missing required data' in data['error']

def test_create_passenger_success(client, init_database, auth_headers):
    response = client.post('/api/create_passenger', headers=auth_headers, json={
        'name': 'Alice Wonderland',
        'age': 28,
        'gender': 'Female',
        'nationality': 'Canadian',
        'scheduled_flights': [],
        'affiliated_passenger_ids': []
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'Passenger created successfully'
    assert data['passenger']['name'] == 'Alice Wonderland'

def test_create_passenger_invalid_data(client, init_database, auth_headers):
    response = client.post('/api/create_passenger', headers=auth_headers, json={
        'name': '',
    })
    assert response.status_code == 400
    assert 'Missing required data' in response.get_json()['error']

