from .base import db
from sqlalchemy import Enum
import enum


class SeaterType(enum.Enum):
    PILOT = 'pilot'
    CABIN_CREW = 'cabin_crew'
    PASSENGER = 'passenger'



class FlightSeatAssignment(db.Model):
    __tablename__ = 'flight_seat_assignment'

    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_number'), primary_key=True, nullable=False)
    seat_map_id = db.Column(db.Integer, db.ForeignKey('seat_map.id'), primary_key=True, nullable=False)
    seater_type = db.Column(Enum(SeaterType), nullable=False)  # Use enum for seater_type
    seater_id = db.Column(db.Integer, nullable=False)  # passenger_id, pilot_id, or cabin_crew_id

    seat_map = db.relationship('SeatMap', backref=db.backref('assignments', lazy=True))

    def __repr__(self):
        return f'<PassengerFlightInfo Passenger ID: {self.seater_id}, Flight ID: {self.flight_id}, Seat: {self.seat_map_id}>'