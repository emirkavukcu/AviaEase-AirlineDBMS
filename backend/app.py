from flask import Flask, url_for, request, jsonify
from config import Config
from models import db
from populate_db import *
from logic import *
import requests

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
            populate_pilots(200)
            print("Pilots populated")
        if CabinCrew.query.first() is None:
            populate_cabin_crew(1000)
            print("Cabin crew populated")
        if Passenger.query.first() is None:
            populate_passengers(5000)
            print("Passengers populated")
        if Airport.query.first() is None:
            populate_airports()

    return app

app = create_app()

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/api/create_flight', methods=['POST'])
def create_flight():
    data = request.get_json()
    required_fields = ['flight_time', 'source', 'destination', 'vehicle_type_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': 'Missing fields', 'missing': missing_fields}), 400
    
    try:
        source_airport = Airport.query.get(data['source'])
        destination_airport = Airport.query.get(data['destination'])

        if not source_airport or not destination_airport:
            return jsonify({"error": "Invalid source or destination airport code"}), 400

        distance = calculate_distance(
            source_airport.longitude, source_airport.latitude,
            destination_airport.longitude, destination_airport.latitude
        )
        # Calculate duration assuming a speed of 15 km/minute
        duration = distance / 15
        flight = Flight(
            airline_code="AE",  # This should be dynamic based on your application's requirements
            date_time=data['flight_time'],
            duration=duration,  # Example duration, you may want to calculate this
            distance=distance,  # Example distance, you may want to calculate this
            source_airport=source_airport.airport_code,
            destination_airport=destination_airport.airport_code,
            aircraft_type_id=data['vehicle_type_id']
        )
        db.session.add(flight)
        db.session.commit()
        seat_plan_auto(flight.flight_number, data['vehicle_type_id'])
        return jsonify({"message": "Flight created successfully", "flight_id": flight.flight_number}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def seat_plan_logic(flight_id, vehicle_type_id):
    # Example logic to create seat plans
    # You'll need to implement this based on your specific requirements
    pass

if __name__ == '__main__':
    app.run(debug=True)
  

if __name__ == '__main__':
    app.run(debug=True)
