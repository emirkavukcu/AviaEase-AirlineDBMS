import pytest
from app import create_app, db
from config import TestConfig
from models import AircraftType, Airport, CabinCrew, Flight, Passenger, Pilot, SeatMap, FlightSeatAssignment
from datetime import datetime


@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def session(app):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db._make_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


def test_aircraft_type(session):
    aircraft_type = AircraftType(
        name="Boeing 737",
        seat_count=138,
        crew_limit=16,
        passenger_limit=122,
        standard_menu=["Chicken", "Vegetarian"]
    )
    session.add(aircraft_type)
    session.commit()

    assert aircraft_type.type_id is not None
    assert aircraft_type.name == "Boeing 737"


def test_airport(session):
    airport = Airport(
        airport_code="JFK",
        name="John F. Kennedy International Airport",
        city="New York",
        country="USA",
        latitude=40.6413,
        longitude=-73.7781
    )
    session.add(airport)
    session.commit()

    assert airport.airport_code == "JFK"
    assert airport.city == "New York"


def test_cabin_crew(session):
    cabin_crew = CabinCrew(
        name="John Doe",
        age=30,
        gender="Male",
        nationality="American",
        known_languages=["English"],
        attendant_type="chief",
        vehicle_type_ids=[1],
        dish_recipes=["Salad", "Pasta"],
        scheduled_flights=[]
    )
    session.add(cabin_crew)
    session.commit()

    assert cabin_crew.attendant_id is not None
    assert cabin_crew.name == "John Doe"


def test_flight(session):
    airport1 = Airport(airport_code="LAX", name="Los Angeles International Airport",
                       city="Los Angeles", country="USA", latitude=33.9416, longitude=-118.4085)
    airport2 = Airport(airport_code="SFO", name="San Francisco International Airport",
                       city="San Francisco", country="USA", latitude=37.7749, longitude=-122.4194)
    aircraft_type = AircraftType(name="Airbus A320", seat_count=138, crew_limit=16,
                                 passenger_limit=122, standard_menu=["Chicken", "Vegetarian"])
    session.add_all([airport1, airport2, aircraft_type])
    session.commit()

    flight = Flight(
        airline_code="AA",
        date_time=datetime(2024, 5, 1, 12, 0, 0),
        duration=120,
        distance=600,
        source_airport="LAX",
        destination_airport="SFO",
        aircraft_type_id=aircraft_type.type_id,
        flight_menu=["Chicken", "Vegetarian"]
    )
    session.add(flight)
    session.commit()

    assert flight.flight_number is not None
    assert flight.airline_code == "AA"


def test_passenger(session):
    passenger = Passenger(
        name="Jane Smith",
        age=25,
        gender="Female",
        nationality="Canadian",
        parent_id=None,
        affiliated_passenger_ids=[],
        scheduled_flights=[]
    )
    session.add(passenger)
    session.commit()

    assert passenger.passenger_id is not None
    assert passenger.name == "Jane Smith"


def test_pilot(session):
    aircraft_type = AircraftType(name="Boeing 777", seat_count=300, crew_limit=20, passenger_limit=280,
                                 standard_menu=["Beef", "Vegetarian"])
    session.add(aircraft_type)
    session.commit()

    pilot = Pilot(
        name="Mike Johnson",
        age=45,
        gender="Male",
        nationality="British",
        known_languages=["English", "French"],
        vehicle_type_id=aircraft_type.type_id,
        allowed_range=10000,
        seniority_level="senior",
        scheduled_flights=[]
    )
    session.add(pilot)
    session.commit()

    assert pilot.pilot_id is not None
    assert pilot.name == "Mike Johnson"


def test_seat_map(session):
    aircraft_type = AircraftType(name="Boeing 787", seat_count=200, crew_limit=18, passenger_limit=182,
                                 standard_menu=["Chicken", "Fish"])
    session.add(aircraft_type)
    session.commit()

    seat_map = SeatMap(
        aircraft_type_id=aircraft_type.type_id,
        seat_row="A",
        seat_number="1",
        seat_type="business",
        seat_group=1,
        seat_group_size=2
    )
    session.add(seat_map)
    session.commit()

    assert seat_map.id is not None
    assert seat_map.seat_row == "A"


def test_flight_seat_assignment(session):
    session.query(FlightSeatAssignment).delete()
    session.query(SeatMap).delete()
    session.query(Passenger).delete()
    session.query(CabinCrew).delete()
    session.query(Pilot).delete()
    session.query(Flight).delete()
    session.query(Airport).delete()
    session.query(AircraftType).delete()
    session.commit()

    aircraft_type = AircraftType(name="Boeing 787", seat_count=200, crew_limit=18, passenger_limit=182,
                                 standard_menu=["Chicken", "Fish"])
    session.add(aircraft_type)
    session.commit()

    airport1 = Airport(airport_code="LAX", name="Los Angeles International Airport", city="Los Angeles",
                       country="USA", latitude=33.9416, longitude=-118.4085)
    airport2 = Airport(airport_code="SFO", name="San Francisco International Airport", city="San Francisco",
                       country="USA", latitude=37.7749, longitude=-122.4194)
    session.add_all([airport1, airport2])
    session.commit()

    flight = Flight(
        airline_code="AA",
        date_time=datetime(2024, 5, 1, 12, 0, 0),
        duration=120,
        distance=600,
        source_airport="LAX",
        destination_airport="SFO",
        aircraft_type_id=aircraft_type.type_id,
        flight_menu=["Chicken", "Fish"]
    )
    session.add(flight)
    session.commit()

    seat_map = SeatMap(
        aircraft_type_id=aircraft_type.type_id,
        seat_row="A",
        seat_number="1",
        seat_type="business",
        seat_group=1,
        seat_group_size=2
    )
    session.add(seat_map)
    session.commit()

    passenger = Passenger(
        name="Jane Smith",
        age=25,
        gender="Female",
        nationality="Canadian",
        parent_id=None,
        affiliated_passenger_ids=[],
        scheduled_flights=[]
    )
    session.add(passenger)
    session.commit()

    flight_seat_assignment = FlightSeatAssignment(
        flight_id=flight.flight_number,
        seat_map_id=seat_map.id,
        seater_type="Passenger",
        seater_id=passenger.passenger_id
    )
    session.add(flight_seat_assignment)
    session.commit()

    assert flight_seat_assignment.flight_id == flight.flight_number
    assert flight_seat_assignment.seat_map_id == seat_map.id
    assert flight_seat_assignment.seater_id == passenger.passenger_id
