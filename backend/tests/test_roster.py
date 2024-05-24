import pytest
from app import create_app, db
from models import Flight, FlightSeatAssignment
from config import TestConfig
from unittest.mock import patch

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
    flight = Flight(flight_number='AB123', aircraft_type_id='Type1')
    db.session.add(flight)
    db.session.commit()

def test_create_roster_auto_missing_fields(client, init_database):
    response = client.post('/create_roster_auto', json={})
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']

@patch('backend.api.roster.FlightSeatAssignment.query')
def test_create_roster_auto_roster_already_exists(mock_query, client, init_database):
    mock_query.filter_by.return_value.first.return_value = True
    response = client.post('/create_roster_auto', json={'flight_number': 'AB123'})
    assert response.status_code == 400
    assert 'A roster for this flight already created' in response.get_json()['message']

@patch('backend.api.roster.Flight.query')
def test_create_roster_auto_invalid_flight_number(mock_query, client, init_database):
    mock_query.filter_by.return_value.first.return_value = None
    response = client.post('/create_roster_auto', json={'flight_number': 'AB123'})
    assert response.status_code == 400
    assert 'Invalid flight number' in response.get_json()['error']

@patch('backend.api.roster.FlightSeatAssignment.query')
@patch('backend.api.roster.Flight.query')
@patch('backend.api.roster.seat_plan_auto')
def test_create_roster_auto_success(mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query, client, init_database):
    mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
    mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
    mock_seat_plan_auto.return_value = "Roster successfully assigned"

    response = client.post('/create_roster_auto', json={'flight_number': 'AB123'})
    assert response.status_code == 201
    assert 'Roster successfully assigned' in response.get_json()['message']

@patch('backend.api.roster.FlightSeatAssignment.query')
@patch('backend.api.roster.Flight.query')
@patch('backend.api.roster.seat_plan_auto')
def test_create_roster_auto_error_in_seat_plan_auto(mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query, client, init_database):
    mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
    mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
    mock_seat_plan_auto.return_value = "Error occurred"

    response = client.post('/create_roster_auto', json={'flight_number': 'AB123'})
    assert response.status_code == 500
    assert 'Error occurred' in response.get_json()['message']

def test_create_roster_auto_no_json(client):
    response = client.post('/create_roster_auto', data='Not a JSON')
    assert response.status_code == 400

def test_create_roster_auto_empty_flight_number(client, init_database):
    response = client.post('/create_roster_auto', json={'flight_number': ''})
    assert response.status_code == 400
    assert 'Invalid flight number' in response.get_json()['error']

def test_create_roster_auto_non_existent_flight(client, init_database):
    response = client.post('/create_roster_auto', json={'flight_number': 'NONEXISTENT'})
    assert response.status_code == 400
    assert 'Invalid flight number' in response.get_json()['error']

def test_create_roster_auto_invalid_json_structure(client):
    response = client.post('/create_roster_auto', json={'invalid_field': 'value'})
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']

@patch('backend.api.roster.FlightSeatAssignment.query')
@patch('backend.api.roster.Flight.query')
@patch('backend.api.roster.seat_plan_auto')
def test_create_roster_auto_seat_plan_auto_exception(mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query, client, init_database):
    mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
    mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
    mock_seat_plan_auto.side_effect = Exception("Unexpected error")

    response = client.post('/create_roster_auto', json={'flight_number': 'AB123'})
    assert response.status_code == 500
    assert 'Unexpected error' in response.get_json()['message']
