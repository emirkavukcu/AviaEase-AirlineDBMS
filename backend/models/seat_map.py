from .base import db
from sqlalchemy import Sequence

seat_map_seq = Sequence('seat_map_seq', start=1, increment=1)


class SeatMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aircraft_type_id = db.Column(db.Integer, db.ForeignKey('aircraft_type.type_id'), nullable=False)
    seat_row = db.Column(db.String(2), nullable=False)
    seat_number = db.Column(db.String(3), nullable=False)  # Including letters for seat designation
    seat_type = db.Column(db.String(50), nullable=False)  # business, economy, crew, etc.
    seat_group = db.Column(db.Integer, nullable=True)  # Group number for seat groups, for adjacent seats
    seat_group_size = db.Column(db.Integer, nullable=True)  # Number of seats in the group
