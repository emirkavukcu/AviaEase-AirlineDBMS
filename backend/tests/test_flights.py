import pytest
from app import create_app, db
from models import Airport, Flight, AircraftType, User
from config import TestConfig
from unittest.mock import patch
from datetime import datetime
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
    # Populate with test users and airport, flight-related data
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user = User(email='test@example.com', password=hashed_password, name='Test User')
    db.session.add(test_user)
    
    airport1 = Airport(
        airport_code="LAX",
        name="Los Angeles International Airport",
        city="Los Angeles",
        country="USA",
        latitude=33.9416,
        longitude=-118.4085
    )
    airport2 = Airport(
        airport_code="SFO",
        name="San Francisco International Airport",
        city="San Francisco",
        country="USA",
        latitude=37.7749,
        longitude=-122.4194
    )
    aircraft_type = AircraftType(
        type_id=1,
        name="Boeing 737",
        seat_count=138,
        crew_limit=16,
        passenger_limit=122,
        standard_menu=["Chicken", "Vegetarian"]
    )
    db.session.add_all([airport1, airport2, aircraft_type])
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

def test_create_flight_missing_fields(client, init_database, auth_headers):
    response = client.post('/api/create_flight', headers=auth_headers, json={})
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']

@patch('services.calculate_distance', return_value=900)
@patch('services.seat_plan_auto', return_value="Seats assigned successfully")
def test_create_flight_success(mock_calculate_distance, mock_seat_plan_auto, client, init_database, auth_headers):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "LAX",
        "destination": "SFO",
        "vehicle_type_id": 1,
        "create_roster": "No"
    }
    response = client.post('/api/create_flight', headers=auth_headers, json=data)
    assert response.status_code == 201
    json_response = response.get_json()
    assert 'Flight succesfully created' in json_response['message']

def test_create_flight_invalid_airport(client, init_database, auth_headers):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "INVALID",
        "destination": "SFO",
        "vehicle_type_id": 1,
        "create_roster": "Yes"
    }
    response = client.post('/api/create_flight', headers=auth_headers, json=data)
    assert response.status_code == 400
    assert 'Invalid source or destination airport code' in response.get_json()['error']

def test_create_flight_invalid_vehicle_type(client, init_database, auth_headers):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "LAX",
        "destination": "SFO",
        "vehicle_type_id": 999,
        "create_roster": "Yes"
    }
    response = client.post('/api/create_flight', headers=auth_headers, json=data)
    assert response.status_code == 400
    assert 'Invalid vehicle type ID' in response.get_json()['error']

@patch('services.calculate_distance', return_value=900)
@patch('services.seat_plan_auto', return_value="Seats assigned successfully")
def test_create_flight_no_roster(mock_calculate_distance, mock_seat_plan_auto, client, init_database, auth_headers):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "LAX",
        "destination": "SFO",
        "vehicle_type_id": 1,
        "create_roster": "No"
    }
    response = client.post('/api/create_flight', headers=auth_headers, json=data)
    assert response.status_code == 201
    json_response = response.get_json()
    assert 'Flight succesfully created' in json_response['message']

def test_get_flights(client, init_database, auth_headers):
    flight = Flight(
        airline_code="AA",
        date_time=datetime(2024, 5, 1, 12, 0, 0),
        duration=120,
        distance=600,
        source_airport="LAX",
        destination_airport="SFO",
        aircraft_type_id=1,
        flight_menu=["Chicken", "Vegetarian"]
    )
    db.session.add(flight)
    db.session.commit()

    response = client.get('/api/flights', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'flights' in data
    assert data['total'] == 1

def test_get_flights_with_filters(client, init_database, auth_headers):
    flight = Flight(
        airline_code="AA",
        date_time=datetime(2024, 5, 1, 12, 0, 0),
        duration=120,
        distance=600,
        source_airport="LAX",
        destination_airport="SFO",
        aircraft_type_id=1,
        flight_menu=["Chicken", "Vegetarian"]
    )
    db.session.add(flight)
    db.session.commit()

    response = client.get('/api/flights?source_airport=LAX&destination_airport=SFO', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'flights' in data
    assert data['total'] == 1
    assert data['flights'][0]['source_airport'] == 'LAX'
    assert data['flights'][0]['destination_airport'] == 'SFO'

