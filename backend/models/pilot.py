from .base import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Enum
import enum


class SeniorityLevel(enum.Enum):
    senior = "senior"
    junior = "junior"
    trainee = "trainee"


class Pilot(db.Model):
    __tablename__ = 'Pilot'
    pilot_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    known_languages = db.Column(ARRAY(db.String), nullable=False)
    vehicle_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_type.type_id'), nullable=False)
    allowed_range = db.Column(db.Integer, nullable=False)
    seniority_level = db.Column(Enum(SeniorityLevel), nullable=False)
    scheduled_flights = db.Column(ARRAY(db.Integer), nullable=False)
    aircraft_type = db.relationship('AircraftType', backref='pilots')

    def __repr__(self):
        return f'<Pilot {self.name}>'
