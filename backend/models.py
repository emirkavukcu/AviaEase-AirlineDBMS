from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Sequence, Integer

db = SQLAlchemy()

flight_number_seq = Sequence('flight_number_seq', start=1000, increment=1)
class Flight(db.Model):
    flight_number = db.Column(db.Integer, flight_number_seq, primary_key=True, server_default=flight_number_seq.next_value())
    airline_code = db.Column(db.String(2), nullable=False) # AE
    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    source_airport = db.Column(db.String, db.ForeignKey('airport.airport_code'), nullable=False)
    destination_airport = db.Column(db.String, db.ForeignKey('airport.airport_code'), nullable=False)
    aircraft_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_type.type_id'), nullable=False)
    flight_menu = db.Column(ARRAY(db.String), nullable=False)
    aircraft_type = db.relationship('AircraftType', backref='flights')
    source = db.relationship('Airport', foreign_keys=[source_airport], backref='departures')
    destination = db.relationship('Airport', foreign_keys=[destination_airport], backref='arrivals')

    def __repr__(self):
        return f'<Flight {self.flight_number}>'
    
class Airport(db.Model):
    airport_code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False) 
    longitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False) 

    def __repr__(self):
        return f'<Airport {self.airport_code} - {self.name}>'

class AircraftType(db.Model):    
    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    seat_count = db.Column(db.Integer, nullable=False)
    crew_limit = db.Column(db.Integer, nullable=False)
    passenger_limit = db.Column(db.Integer, nullable=False)
    standard_menu = db.Column(ARRAY(db.String), nullable=False) 

seat_map_seq = Sequence('seat_map_seq', start=1, increment=1)
class SeatMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aircraft_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_type.type_id'), nullable=False, server_default=flight_number_seq.next_value())
    seat_row = db.Column(db.String(2), nullable=False)
    seat_number = db.Column(db.String(3), nullable=False)  # Including letters for seat designation
    seat_type = db.Column(db.String(50), nullable=False)  # business, economy, crew, etc.

class Pilot(db.Model):
    __tablename__ = 'pilot'
    pilot_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    known_languages = db.Column(ARRAY(db.String), nullable=False) 
    vehicle_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_type.type_id'), nullable=False)
    allowed_range = db.Column(db.Integer, nullable=False) # Maximum distance in kilometers
    seniority_level = db.Column(db.String(50), nullable=False) # Enum ('senior', 'junior', 'trainee') could be used
    scheduled_flights = db.Column(ARRAY(db.String), nullable=False) # List of Flight.flight_number values
    aircraft_type = db.relationship('AircraftType', backref='pilots')

    def __repr__(self):
        return f'<Pilot {self.name}>'
    
class CabinCrew(db.Model):
    __tablename__ = 'cabin_crew'
    attendant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    known_languages = db.Column(ARRAY(db.String), nullable=False)
    attendant_type = db.Column(db.String(50), nullable=False) # 'chief', 'regular', 'chef'
    vehicle_type_ids = db.Column(ARRAY(db.Integer), nullable=False) # List of AircraftType.type_id values
    dish_recipes = db.Column(ARRAY(db.String), nullable=True) # Relevant only for chefs
    scheduled_flights = db.Column(ARRAY(db.String), nullable=False) # List of Flight.flight_number values

    def __repr__(self):
        return f'<CabinCrew {self.name}>'    
    
class Passenger(db.Model):
    __tablename__ = 'passenger'
    passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('passenger.passenger_id'), nullable=True) # For infants
    affiliated_passenger_ids = db.Column(ARRAY(db.Integer), nullable=True) # List of Passenger.passenger_id values
    scheduled_flights = db.Column(ARRAY(db.String), nullable=False) # List of Flight.flight_number values

    parent = db.relationship('Passenger', remote_side=[passenger_id], backref='children')

    def __repr__(self):
        return f'<Passenger {self.name}>'
    
class FlightSeatAssignment(db.Model):
    __tablename__ = 'flight_seat_assignment'
    
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_number'), primary_key=True, nullable=False)
    seat_map_id = db.Column(db.Integer, db.ForeignKey('seat_map.id'), primary_key=True, nullable=False)
    seater_type = db.Column(db.String(50), nullable=False)  # 'pilot', 'cabin_crew', 'passenger'
    seater_id = db.Column(db.Integer, nullable=False) # passenger_id, pilot_id, or cabin_crew_id

    def __repr__(self):
        return f'<PassengerFlightInfo Passenger ID: {self.passenger_id}, Flight ID: {self.flight_id}, Seat: {self.seat_row}{self.seat_number}>'
