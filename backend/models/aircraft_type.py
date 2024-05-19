from .base import db
from sqlalchemy.dialects.postgresql import ARRAY


class AircraftType(db.Model):    
    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    seat_count = db.Column(db.Integer, nullable=False)
    crew_limit = db.Column(db.Integer, nullable=False)
    passenger_limit = db.Column(db.Integer, nullable=False)
    standard_menu = db.Column(ARRAY(db.String), nullable=False)
