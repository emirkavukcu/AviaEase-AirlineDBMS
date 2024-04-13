from .base import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Sequence, Integer

flight_number_seq = Sequence('flight_number_seq', start=1000, increment=1)
class Flight(db.Model):
    flight_number = db.Column(db.Integer, flight_number_seq, primary_key=True, server_default=flight_number_seq.next_value())
    airline_code = db.Column(db.String(2), nullable=False) # AE
    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    source_airport = db.Column(db.String, db.ForeignKey('airport.airport_code'), nullable=False)
    destination_airport = db.Column(db.String, db.ForeignKey('airport.airport_code'), nullable=False)
    aircraft_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_type.type_id'), nullable=False)
    flight_menu = db.Column(ARRAY(db.String), nullable=False)
    aircraft_type = db.relationship('AircraftType', backref='flights')
    source = db.relationship('Airport', foreign_keys=[source_airport], backref='departures')
    destination = db.relationship('Airport', foreign_keys=[destination_airport], backref='arrivals')

    def __repr__(self):
        return f'<Flight {self.flight_number}>'