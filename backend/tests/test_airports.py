import pytest
from app import create_app, db
from models.airport import Airport
from models.user import User  # Import the User model
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
    # Populate with test users and airport data
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user = User(email='test@example.com', password=hashed_password, name='Test User')
    db.session.add(test_user)

    airport1 = Airport(
        airport_code='AAA',
        name='Sample Airport 1',
        city='Sample City 1',
        country='AA',
        latitude=12.345678,
        longitude=98.765432
    )
    airport2 = Airport(
        airport_code='ZZZ',
        name='Sample Airport 2',
        city='Sample City 2',
        country='ZZ',
        latitude=23.456789,
        longitude=87.654321
    )
    db.session.add(airport1)
    db.session.add(airport2)
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

def test_get_airport_codes(client, init_database, auth_headers):
    response = client.get('/api/airport_codes', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert 'AAA' in data
    assert 'ZZZ' in data

def test_get_airport_details(client, init_database, auth_headers):
    response = client.get('/api/airports', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert any(airport['airport_code'] == 'AAA' and airport['city'] == 'Sample City 1' and airport['country'] == 'AA' for airport in data)
    assert any(airport['airport_code'] == 'ZZZ' and airport['city'] == 'Sample City 2' and airport['country'] == 'ZZ' for airport in data)

def test_get_airport_details_country_code(client, init_database, auth_headers):
    response = client.get('/api/airports', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert any(airport['country'] == 'AA' for airport in data)

def test_get_airport_details_country_name(client, init_database, auth_headers):
    response = client.get('/api/airports', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert any(airport['country'] == 'AA' for airport in data)

def test_get_airport_codes_specific_airport(client, init_database, auth_headers):
    response = client.get('/api/airport_codes', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert 'AAA' in data

def test_get_airport_details_specific_airport(client, init_database, auth_headers):
    response = client.get('/api/airports', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert any(airport['airport_code'] == 'AAA' for airport in data)

def test_get_airport_codes_multiple_airports(client, init_database, auth_headers):
    response = client.get('/api/airport_codes', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert 'AAA' in data
    assert 'ZZZ' in data

def test_get_airport_details_multiple_airports(client, init_database, auth_headers):
    response = client.get('/api/airports', headers=auth_headers)
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert any(airport['airport_code'] == 'AAA' for airport in data)
    assert any(airport['airport_code'] == 'ZZZ' for airport in data)
