import pytest
from app import create_app, db
from models import Airport, Flight, AircraftType
from config import TestConfig
from unittest.mock import patch
from datetime import datetime

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

def test_create_flight_missing_fields(client, init_database):
    response = client.post('/create_flight', json={})
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']

@patch('services.calculate_distance', return_value=900)
@patch('services.seat_plan_auto', return_value="Seats assigned successfully")
def test_create_flight_success(mock_calculate_distance, mock_seat_plan_auto, client, init_database):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "LAX",
        "destination": "SFO",
        "vehicle_type_id": 1,
        "create_roster": "Yes"
    }
    response = client.post('/create_flight', json=data)
    assert response.status_code == 201
    json_response = response.get_json()
    assert 'Flight created and roster successfully assigned' in json_response['message']

def test_create_flight_invalid_airport(client, init_database):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "INVALID",
        "destination": "SFO",
        "vehicle_type_id": 1,
        "create_roster": "Yes"
    }
    response = client.post('/create_flight', json=data)
    assert response.status_code == 400
    assert 'Invalid source or destination airport code' in response.get_json()['error']

def test_create_flight_invalid_vehicle_type(client, init_database):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "LAX",
        "destination": "SFO",
        "vehicle_type_id": 999,
        "create_roster": "Yes"
    }
    response = client.post('/create_flight', json=data)
    assert response.status_code == 400
    assert 'Invalid vehicle type ID' in response.get_json()['error']

@patch('services.calculate_distance', return_value=900)
@patch('services.seat_plan_auto', return_value="Seats assigned successfully")
def test_create_flight_no_roster(mock_calculate_distance, mock_seat_plan_auto, client, init_database):
    data = {
        "flight_time": "2024-05-01T12:00:00",
        "source": "LAX",
        "destination": "SFO",
        "vehicle_type_id": 1,
        "create_roster": "No"
    }
    response = client.post('/create_flight', json=data)
    assert response.status_code == 201
    json_response = response.get_json()
    assert 'Flight succesfully created' in json_response['message']

def test_get_flights(client, init_database):
    populate_db()
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

    response = client.get('/flights')
    assert response.status_code == 200
    data = response.get_json()
    assert 'flights' in data
    assert data['total'] == 1

def test_get_flights_with_filters(client, init_database):
    populate_db()
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

    response = client.get('/flights?source_airport=LAX&destination_airport=SFO')
    assert response.status_code == 200
    data = response.get_json()
    assert 'flights' in data
    assert data['total'] == 1
    assert data['flights'][0]['source_airport'] == 'LAX'
    assert data['flights'][0]['destination_airport'] == 'SFO'
