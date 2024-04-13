from flask import Blueprint, jsonify, request
from models import Flight, FlightSeatAssignment
from services import seat_plan_auto

roster = Blueprint('roster', __name__)

@roster.route('/create_roster_auto', methods=['POST'])
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
