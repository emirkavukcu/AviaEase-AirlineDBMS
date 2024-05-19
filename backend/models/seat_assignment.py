from .base import db


class FlightSeatAssignment(db.Model):
    __tablename__ = 'flight_seat_assignment'
    
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_number'), primary_key=True, nullable=False)
    seat_map_id = db.Column(db.Integer, db.ForeignKey('seat_map.id'), primary_key=True, nullable=False)
    seater_type = db.Column(db.String(50), nullable=False)  # 'pilot', 'cabin_crew', 'passenger'
    seater_id = db.Column(db.Integer, nullable=False)  # passenger_id, pilot_id, or cabin_crew_id

    seat_map = db.relationship('SeatMap', backref=db.backref('assignments', lazy=True))

    def __repr__(self):
        return (f'<PassengerFlightInfo Passenger ID: {self.passenger_id}, Flight ID: {self.flight_id}, '
                f'Seat: {self.seat_row}{self.seat_number}>')
