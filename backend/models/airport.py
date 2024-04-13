from .base import db

class Airport(db.Model):
    airport_code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False) 
    longitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False) 

    def __repr__(self):
        return f'<Airport {self.airport_code} - {self.name}>'