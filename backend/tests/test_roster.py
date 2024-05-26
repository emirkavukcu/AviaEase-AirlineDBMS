import pytest
from app import create_app, db
from models import Flight, FlightSeatAssignment, Airport, AircraftType
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
    source_airport = Airport(airport_code='XY', name='Sample Airport XY', city='Sample City XY',
                             country='Sample Country XY', latitude=1.0, longitude=2.0)
    destination_airport = Airport(airport_code='AB', name='Sample Airport AB', city='Sample City AB',
                                  country='Sample Country AB', latitude=3.0, longitude=4.0)
    db.session.add(source_airport)
    db.session.add(destination_airport)

    aircraft_type = AircraftType(type_id=1, name="Boeing 737", seat_count=138, crew_limit=16, passenger_limit=122,
                                 standard_menu=['Food', 'Drink'])
    db.session.add(aircraft_type)

    flight = Flight(flight_number=1, airline_code='AB',
                    date_time=datetime(2024, 5, 1, 12, 0, 0),
                    duration=120.0, distance=1000, source_airport='XY', destination_airport='AB',
                    aircraft_type_id=1, flight_menu=['Food', 'Drink'])
    db.session.add(flight)
    db.session.commit()


def test_create_roster_auto_missing_fields(client, init_database):
    response = client.post('/create_roster_auto', json={})
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']


@patch('models.FlightSeatAssignment.query')
def test_create_roster_auto_roster_already_exists(mock_query, client, init_database):
    mock_query.filter_by.return_value.first.return_value = True
    response = client.post('/create_roster_auto', json={'flight_number': 'AB123'})
    assert response.status_code == 400
    assert 'A roster for this flight already created' in response.get_json()['message']


@patch('models.Flight.query')
def test_create_roster_auto_invalid_flight_number(mock_query, client, init_database):
    mock_query.filter_by.return_value.first.return_value = None
    response = client.post('/create_roster_auto', json={'flight_number': 99999})
    assert response.status_code == 400
    assert 'Invalid flight number' in response.get_json()['error']


@patch('models.FlightSeatAssignment.query')
@patch('models.Flight.query')
@patch('services.seat_plan_auto')
def test_create_roster_auto_success(mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query, client,
                                    init_database):
    mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
    mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number=1001,
                                                                         aircraft_type_id=1)
    mock_seat_plan_auto.return_value = "Roster successfully assigned"

    response = client.post('/create_roster_auto', json={'flight_number': 1001})
    assert response.status_code == 201
    assert 'Roster successfully assigned' in response.get_json()['message']


@patch('models.FlightSeatAssignment.query')
@patch('models.Flight.query')
@patch('services.seat_plan_auto')
def test_create_roster_auto_error_in_seat_plan_auto(mock_seat_plan_auto, mock_flight_query,
                                                    mock_flight_seat_assignment_query, client, init_database):
    mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
    mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123',
                                                                         aircraft_type_id=1)
    mock_seat_plan_auto.return_value = "Error occurred"

    response = client.post('/create_roster_auto', json={'flight_number': 'AB123'})
    assert response.status_code == 500
    assert 'Error occurred' in response.get_json()['message']


def test_create_roster_auto_no_json(client):
    response = client.post('/create_roster_auto', data='Not a JSON')
    assert response.status_code == 415


def test_create_roster_auto_empty_flight_number(client, init_database):
    response = client.post('/create_roster_auto', json={'flight_number': None})
    assert response.status_code == 400
    assert 'Invalid flight number' in response.get_json()['error']


def test_create_roster_auto_non_existent_flight(client, init_database):
    response = client.post('/create_roster_auto', json={'flight_number': 9999})
    assert response.status_code == 400
    assert 'Invalid flight number' in response.get_json()['error']


def test_create_roster_auto_invalid_json_structure(client):
    response = client.post('/create_roster_auto', json={'invalid_field': 'value'})
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']


@patch('models.FlightSeatAssignment.query')
@patch('models.Flight.query')
@patch('services.seat_plan_auto')
def test_create_roster_auto_seat_plan_auto_exception(mock_seat_plan_auto, mock_flight_query,
                                                     mock_flight_seat_assignment_query, client, init_database):
    mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
    mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number=123,
                                                                         aircraft_type_id=1)
    mock_seat_plan_auto.side_effect = Exception("Unexpected error")

    response = client.post('/create_roster_auto', json={'flight_number': 123})
    assert response.status_code == 500
    assert 'Unexpected error' in response.get_json()['message']
