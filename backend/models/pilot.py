from sqlalchemy import SmallInteger
from .base import db
from sqlalchemy.dialects.postgresql import ARRAY


class Pilot(db.Model):
    __tablename__ = 'pilot'
    pilot_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(SmallInteger, nullable=False)  # ISO 5218
    nationality = db.Column(db.String(3), nullable=False)  # ISO 3166-1 alpha-3
    known_languages = db.Column(ARRAY(db.String), nullable=False) 
    vehicle_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_type.type_id'), nullable=False)
    allowed_range = db.Column(db.Integer, nullable=False)  # Maximum distance in kilometers
    seniority_level = db.Column(db.String(50), nullable=False)  # Enum ('senior', 'junior', 'trainee') could be used
    scheduled_flights = db.Column(ARRAY(db.Integer), nullable=False)  # List of Flight.flight_number values
    aircraft_type = db.relationship('AircraftType', backref='pilots')

    def __repr__(self):
        return f'<Pilot {self.name}>'
