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
    required_fields = ['flight_time', 'source', 'destination', 'vehicle_type_id', 'create_roster']
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
        duration = distance / 15  # Calculate duration assuming a speed of 15 km/minute

        # Retrieve the flight menu from the aircraft type
        aircraft_type = AircraftType.query.get(data['vehicle_type_id'])
        if not aircraft_type:
            return jsonify({"error": "Invalid vehicle type ID"}), 400

        flight = Flight(
            airline_code="AE",  
            date_time=data['flight_time'],
            duration=duration,  
            distance=distance, 
            source_airport=source_airport.airport_code,
            destination_airport=destination_airport.airport_code,
            aircraft_type_id=data['vehicle_type_id'],
            flight_menu=aircraft_type.standard_menu  # Use the standard menu from the aircraft type
        )
        db.session.add(flight)
        db.session.commit()

        if data['create_roster'] == "No":
            return jsonify({"message": "Flight succesfully created", "flight_id": flight.flight_number}), 201
        
        elif data['create_roster'] == "Yes":
          returnedMessage = seat_plan_auto(flight.flight_number, data['vehicle_type_id'])
          if returnedMessage != "Seats successfully assigned":
              return jsonify({"message": returnedMessage}), 500
          else:
            message = "Flight created and roster successfully assigned"
            return jsonify({"message": message, "flight_id": flight.flight_number}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/create_roster_auto', methods=['POST'])
def create_roster_auto():
    data = request.get_json()
    required_fields = ['flight_number']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': 'Missing fields', 'missing': missing_fields}), 400
    
    flight_number = data['flight_number']
    if FlightSeatAssignment.query.filter_by(flight_id=flight_number).first():
      return jsonify({"message": "A roster for this flight already created"}), 400

    flight = Flight.query.filter_by(flight_number=flight_number).first()
    if not flight:
      return jsonify({"error": "Invalid flight number"}), 400

    vehicle_type_id = flight.aircraft_type_id

    returnedMessage = seat_plan_auto(flight_number, vehicle_type_id)
    if returnedMessage != "Roster successfully assigned":
      return jsonify({"message": returnedMessage}), 500
    else:
      return jsonify({"message": returnedMessage}), 201

if __name__ == '__main__':
    app.run(debug=True)