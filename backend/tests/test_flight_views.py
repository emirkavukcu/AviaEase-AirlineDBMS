import pytest
from app import create_app, db
from models import Flight, FlightSeatAssignment, Passenger, Pilot, CabinCrew, SeatMap, Airport, AircraftType, User
from config import TestConfig
import json
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
    # Populate with test users and flight-related data
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user = User(email='test@example.com', password=hashed_password, name='Test User')
    db.session.add(test_user)
    
    airport1 = Airport(airport_code='XY', name='Sample Airport XY', city='Sample City XY', country='Sample Country XY', latitude=1.0, longitude=2.0)
    airport2 = Airport(airport_code='AB', name='Sample Airport AB', city='Sample City AB', country='Sample Country AB', latitude=3.0, longitude=4.0)
    db.session.add(airport1)
    db.session.add(airport2)

    aircraft_type = AircraftType(type_id=1, name='Boeing 737', seat_count=5, crew_limit=3, passenger_limit=150, standard_menu=['Food', 'Drink'])
    db.session.add(aircraft_type)

    seat_map1 = SeatMap(id=1, seat_row='A', seat_number=1, seat_type='Economy', aircraft_type_id=aircraft_type.type_id)
    seat_map2 = SeatMap(id=2, seat_row='A', seat_number=2, seat_type='Business', aircraft_type_id=aircraft_type.type_id)
    db.session.add(seat_map1)
    db.session.add(seat_map2)

    pilot = Pilot(pilot_id=1, name='John Doe', age=40, gender='Male', nationality='American', known_languages=['English'], seniority_level='Senior', vehicle_type_id=1, allowed_range=500, scheduled_flights=[1009, 1010, 1011])
    cabin_crew = CabinCrew(attendant_id=2, name='Jane Smith', age=30, gender='Female', nationality='Canadian', known_languages=['English', 'French'], attendant_type='Chief', vehicle_type_ids=[1], dish_recipes=None, scheduled_flights=[1006, 1007, 1008])
    passenger = Passenger(name='Alice Johnson', age=25, gender='Female', nationality='British', parent_id=None, affiliated_passenger_ids=[], scheduled_flights=[1003, 1004, 1005])
    db.session.add(pilot)
    db.session.add(cabin_crew)
    db.session.add(passenger)

    flight = Flight(flight_number=1, airline_code='AB', date_time=datetime(2024, 5, 1, 12, 0, 0), duration=120, distance=1000, source_airport='XY', destination_airport='AB', aircraft_type_id=1, flight_menu=['Food', 'Drink'])
    db.session.add(flight)

    assignment1 = FlightSeatAssignment(flight_id=flight.flight_number, seater_id=pilot.pilot_id, seater_type='SeniorPilot', seat_map_id=seat_map1.id)
    assignment2 = FlightSeatAssignment(flight_id=flight.flight_number, seater_id=cabin_crew.attendant_id, seater_type='ChiefCabinCrew', seat_map_id=seat_map2.id)
    db.session.add(assignment1)
    db.session.add(assignment2)
    db.session.commit()  # Ensure data is committed to the database

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

def test_tabular_view(client, init_database, auth_headers):
    response = client.get('/api/1/tabular_view', headers=auth_headers)
    data = response.get_json()
    print("Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data) == 2  # Assuming two seat assignments

def test_plane_view(client, init_database, auth_headers):
    response = client.get('/api/1/plane_view', headers=auth_headers)
    data = response.get_json()
    print("Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data) == 2  # Assuming two seat assignments

def test_extended_view(client, init_database, auth_headers):
    response = client.get('/api/1/extended_view', headers=auth_headers)
    data = response.get_json()
    print("Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data) == 3  # Assuming flight_crew_data, cabin_crew_data, passenger_data

def test_invalid_flight_tabular_view(client, init_database, auth_headers):
    response = client.get('/api/999/tabular_view', headers=auth_headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Flight not found'

def test_invalid_flight_plane_view(client, init_database, auth_headers):
    response = client.get('/api/999/plane_view', headers=auth_headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Flight not found'

def test_invalid_flight_extended_view(client, init_database, auth_headers):
    response = client.get('/api/999/extended_view', headers=auth_headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Flight not found'

