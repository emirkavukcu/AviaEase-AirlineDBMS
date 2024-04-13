from flask import Flask
from config import Config
from models import db
from populate_db import *
from api import register_blueprints  

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        # Import models here to ensure they are known to SQLAlchemy
        from models import Flight, SeatMap, AircraftType, Airport, Pilot, CabinCrew, Passenger, FlightSeatAssignment

        db.create_all()
        # Populate the tables if they are empty
        if AircraftType.query.first() is None:
            populate_aircraft_types()  
        if SeatMap.query.first() is None:
            populate_seatmaps()
        if Pilot.query.first() is None:
            populate_pilots(500)
            print("Pilots populated")
        if CabinCrew.query.first() is None:
            populate_cabin_crew(2000)
            print("Cabin crew populated")
        if Passenger.query.first() is None:
            populate_passengers(20000)
            print("Passengers populated")
        if Airport.query.first() is None:
            populate_airports()
        if Flight.query.first() is None:
            start_date = datetime(2024, 5, 1)
            end_date = datetime(2024, 12, 31)
            populate_flights_with_rosters(start_date, end_date, 100)
            print("Flights populated")
    
    register_blueprints(app)
    return app

app = create_app()

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
