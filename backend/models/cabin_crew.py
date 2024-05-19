from sqlalchemy import SmallInteger
from .base import db
from sqlalchemy.dialects.postgresql import ARRAY


class CabinCrew(db.Model):
    __tablename__ = 'cabin_crew'
    attendant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(SmallInteger, nullable=False)  # ISO 5218
    nationality = db.Column(db.String(3), nullable=False)  # ISO 3166-1 alpha-3
    known_languages = db.Column(ARRAY(db.String), nullable=False)
    attendant_type = db.Column(db.String(50), nullable=False)  # 'chief', 'regular', 'chef'
    vehicle_type_ids = db.Column(ARRAY(db.Integer), nullable=False)  # List of AircraftType.type_id values
    dish_recipes = db.Column(ARRAY(db.String), nullable=True)  # Relevant only for chefs
    scheduled_flights = db.Column(ARRAY(db.Integer), nullable=False)  # List of Flight.flight_number values

    def __repr__(self):
        return f'<CabinCrew {self.name}>'
