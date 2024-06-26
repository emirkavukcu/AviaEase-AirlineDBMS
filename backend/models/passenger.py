from .base import db
from sqlalchemy.dialects.postgresql import ARRAY

class Passenger(db.Model):
    __tablename__ = 'passenger'
    passenger_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('passenger.passenger_id'), nullable=True) # For infants
    affiliated_passenger_ids = db.Column(ARRAY(db.Integer), nullable=True) # List of Passenger.passenger_id values
    scheduled_flights = db.Column(ARRAY(db.Integer), nullable=False) # List of Flight.flight_number values

    parent = db.relationship('Passenger', remote_side=[passenger_id], backref='children')

    def __repr__(self):
        return f'<Passenger {self.name}>'