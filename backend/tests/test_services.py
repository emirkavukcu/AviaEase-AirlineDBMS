import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from app import create_app
from models import db, Flight, Pilot, CabinCrew, Passenger, SeatMap, Airport, AircraftType
from services.availability_service import find_available_pilots, find_available_cabin_crew, find_available_passengers, scheduleIsAvailable
from services.distance_service import calculate_distance
from services.seat_assignment_service import seat_plan_auto
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
    source_airport = Airport(airport_code='XY', name='Sample Airport XY', city='Sample City XY',
                             country='Sample Country XY', latitude=1.0, longitude=2.0)
    destination_airport = Airport(airport_code='AB', name='Sample Airport AB', city='Sample City AB',
                                  country='Sample Country AB', latitude=3.0, longitude=4.0)
    db.session.add(source_airport)
    db.session.add(destination_airport)
    db.session.commit()

    aircraft_type = AircraftType(type_id=1, name="Boeing 737", seat_count=138, crew_limit=16, passenger_limit=122,
                                 standard_menu=['Food', 'Drink'])
    db.session.add(aircraft_type)
    db.session.commit()

    flight = Flight(flight_number=1, airline_code='AB',
                    date_time=datetime(2024, 5, 1, 12, 0, 0),
                    duration=120, distance=1000, source_airport='XY', destination_airport='AB',
                    aircraft_type_id=1, flight_menu=['Food', 'Drink'])
    db.session.add(flight)
    db.session.commit()

    for i in range(10):
        pilot = Pilot(pilot_id=i+1, name=f'John Doe {i+1}', age=40, gender='Male', nationality='American',
                      known_languages=['English'], seniority_level='Senior', vehicle_type_id=1, allowed_range=2000,
                      scheduled_flights=[])
        db.session.add(pilot)

    for i in range(10):
        cabin_crew = CabinCrew(attendant_id=i+1, name=f'Jane Doe {i+1}', age=30, gender='Female', nationality='Canadian',
                               known_languages=['English'], attendant_type='Chief', vehicle_type_ids=[1],
                               dish_recipes=[], scheduled_flights=[])
        db.session.add(cabin_crew)

    for i in range(10):
        passenger = Passenger(passenger_id=i+1, name=f'Alice {i+1}', age=25, gender='Female', nationality='British',
                              parent_id=None, affiliated_passenger_ids=[], scheduled_flights=[])
        db.session.add(passenger)

    for i in range(10):
        seat_map = SeatMap(id=i+1, seat_row='A', seat_number=i+1, seat_type='Economy', aircraft_type_id=1)
        db.session.add(seat_map)

    for i in range(1, 4):  # Adding pilot seats
        seat_map = SeatMap(id=11+i, seat_row='PL', seat_number=i, seat_type='pilot', aircraft_type_id=1)
        db.session.add(seat_map)

    for i in range(1, 13):  # Adding extra seats for testing, covering the potential seat_map_id 26
        seat_map = SeatMap(id=14+i, seat_row='B', seat_number=i, seat_type='Economy', aircraft_type_id=1)
        db.session.add(seat_map)

    db.session.commit()


def test_schedule_is_available(app, init_database):
    with app.app_context():
        start_time = datetime(2024, 5, 1, 12, 0, 0)
        end_time = start_time + timedelta(hours=2)
        result = scheduleIsAvailable(start_time, end_time, Pilot, 1)
        assert result is True  # Updated based on your current data

def test_find_available_pilots(app, init_database):
    with app.app_context():
        result = find_available_pilots(1, 'Senior', 1)
        assert isinstance(result, list)
        assert len(result) == 1

def test_find_available_cabin_crew(app, init_database):
    with app.app_context():
        result = find_available_cabin_crew(1, 'Chief', 1)
        assert isinstance(result, list)
        assert len(result) == 1

def test_find_available_passengers(app, init_database):
    with app.app_context():
        result = find_available_passengers(1, 1)
        assert isinstance(result, list)
        assert len(result) == 1

def test_calculate_distance(app, init_database):
    with app.app_context():
        result = calculate_distance(1.0, 2.0, 3.0, 4.0)
        assert isinstance(result, float)

@patch('services.seat_assignment_service.find_available_pilots')
@patch('services.seat_assignment_service.find_available_cabin_crew')
@patch('services.seat_assignment_service.find_available_passengers')
def test_seat_plan_auto(mock_find_available_pilots, mock_find_available_cabin_crew, mock_find_available_passengers, app, init_database):
    with app.app_context():
        mock_find_available_pilots.return_value = [1]
        mock_find_available_cabin_crew.return_value = [1]
        mock_find_available_passengers.return_value = [1]

        result = seat_plan_auto(1, 1)
        assert result == "Seats assigned successfully"

