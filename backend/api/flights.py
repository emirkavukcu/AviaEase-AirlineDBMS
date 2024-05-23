from flask import Blueprint, jsonify, request
from models import db, Airport, Flight, AircraftType
from services import calculate_distance, seat_plan_auto
from datetime import datetime, timedelta
from sqlalchemy import cast, String 
from sqlalchemy.orm import aliased

flights = Blueprint('flights', __name__)

# Endpoint to create a flight
@flights.route('/create_flight', methods=['POST'])
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
        duration = distance / 15  # Speed assumption: 15 km/minute, duration is in minutes

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
          returnedMessage = seat_plan_auto(flight.flight_number, flight.aircraft_type_id)
          if returnedMessage != "Seats assigned successfully":
              return jsonify({"message": returnedMessage}), 500
          else:
            message = "Flight created and roster successfully assigned"
            return jsonify({"message": message, "flight_id": flight.flight_number}), 201
        
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500
    
# Endpoint to get flights with filtering and pagination 
@flights.route('/flights', methods=['GET'])
def get_flights():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Filter parameters
    flight_number_prefix = request.args.get('flight_number')
    min_date_time = request.args.get('min_date_time')
    max_date_time = request.args.get('max_date_time')
    min_duration = request.args.get('min_duration', type=int)
    max_duration = request.args.get('max_duration', type=int)
    min_distance = request.args.get('min_distance', type=float)
    max_distance = request.args.get('max_distance', type=float)
    source_airport = request.args.get('source_airport')
    destination_airport = request.args.get('destination_airport')
    source_city = request.args.get('source_city')
    destination_city = request.args.get('destination_city')
    source_country = request.args.get('source_country')
    destination_country = request.args.get('destination_country')

    query = Flight.query

    # Apply filters
    if flight_number_prefix:
        query = query.filter(cast(Flight.flight_number, String).like(f"{flight_number_prefix}%"))
    if min_date_time:
        query = query.filter(Flight.date_time >= datetime.fromisoformat(min_date_time))
    if max_date_time:
        query = query.filter(Flight.date_time <= datetime.fromisoformat(max_date_time))
    if min_duration is not None:
        query = query.filter(Flight.duration >= min_duration)
    if max_duration is not None:
        query = query.filter(Flight.duration <= max_duration)
    if min_distance is not None:
        query = query.filter(Flight.distance >= min_distance)
    if max_distance is not None:
        query = query.filter(Flight.distance <= max_distance)
    if source_airport:
        query = query.filter(Flight.source_airport.ilike(source_airport))
    if destination_airport:
        query = query.filter(Flight.destination_airport.ilike(destination_airport))

    # Join with Airport to filter by city or country
    source_airport_alias = aliased(Airport)
    destination_airport_alias = aliased(Airport)
    
    query = query.join(source_airport_alias, Flight.source_airport == source_airport_alias.airport_code)
    query = query.join(destination_airport_alias, Flight.destination_airport == destination_airport_alias.airport_code)

    if source_city:
        query = query.filter(source_airport_alias.city.ilike(source_city))
    if source_country:
        query = query.filter(source_airport_alias.country.ilike(source_country))

    if destination_city:
        query = query.filter(destination_airport_alias.city.ilike(destination_city))
    if destination_country:
        query = query.filter(destination_airport_alias.country.ilike(destination_country))

    # Select the fields you want to include in the result
    query = query.add_columns(
        source_airport_alias.country.label('source_country'),
        source_airport_alias.city.label('source_city'),
        destination_airport_alias.country.label('destination_country'),
        destination_airport_alias.city.label('destination_city')
    )

    # Sort by flight_number
    query = query.order_by(Flight.flight_number)

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    flights = pagination.items

    # Serialize flights
    flights_data = [{
      "flight_number": flight.Flight.flight_number,
      "airline_code": flight.Flight.airline_code,
      "date_time": flight.Flight.date_time.isoformat(),
      "duration": flight.Flight.duration,
      "distance": flight.Flight.distance,
      "source_airport": flight.Flight.source_airport,
      "destination_airport": flight.Flight.destination_airport,
      "aircraft_type_id": flight.Flight.aircraft_type_id,
      "aircraft_type": "Boeing 737" if flight.Flight.aircraft_type_id == 1 
               else "Airbus A320" if flight.Flight.aircraft_type_id == 2 
               else "Boeing 777" if flight.Flight.aircraft_type_id == 3 
               else "Unknown",
      "status": "passed" if flight.Flight.date_time + timedelta(minutes=flight.Flight.duration) < datetime.now() 
           else "active" if flight.Flight.date_time <= datetime.now() 
           else "pending",
      "source_country": flight.source_country,
      "source_city": flight.source_city,
      "destination_country": flight.destination_country,
      "destination_city": flight.destination_city,
      "flight_menu": flight.Flight.flight_menu
    } for flight in flights]

    # Response with pagination metadata
    response = {
        "flights": flights_data,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }

    return jsonify(response), 200



