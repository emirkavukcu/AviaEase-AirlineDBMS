from flask import Flask, jsonify, request
from config import Config, TestConfig
from models import db
from populate_db import *
from api import register_blueprints
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv

load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

    db.init_app(app)

    jwt = JWTManager(app)

    with app.app_context():
        # Import models here to ensure they are known to SQLAlchemy
        from models import Flight, SeatMap, AircraftType, Airport, Pilot, CabinCrew, Passenger, FlightSeatAssignment, User

        db.create_all()
        # Populate the tables if they are empty
        if not app.config['TESTING']:  # Only populate for non-test environments
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
    return jsonify({"message": "Welcome to the Airline DBMS API"}), 200

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)

