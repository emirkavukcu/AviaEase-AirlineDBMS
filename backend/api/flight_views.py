from flask import Blueprint, request, jsonify
from models import db, CabinCrew, FlightSeatAssignment, Passenger, Pilot, Flight, SeatMap

flight_views = Blueprint('flight_views', __name__)

@flight_views.route('/<int:flight_id>/tabular_view', methods=['GET'])
def tabular_view(flight_id: int):
    # Check if flight exists
    if not Flight.query.get(flight_id):
        return jsonify({"error": "Flight not found"}), 404

    # Fetch seat assignments for the specific flight
    assignments = FlightSeatAssignment.query.filter_by(flight_id=flight_id).all()

    data = []
    for assignment in assignments:
        person_type = assignment.seater_type
        person_data = {}

        if person_type == "Passenger":
            person = Passenger.query.get(assignment.seater_id)
            person_data.update({"name": person.name, "id": person.passenger_id, "person_type": person_type})

        elif person_type in ["SeniorPilot", "JuniorPilot", "TraineePilot"]:
            person = Pilot.query.get(assignment.seater_id)
            # Format the person type by inserting a space before "Pilot"
            formatted_type = person_type.replace("Pilot", " Pilot")
            person_data.update({"name": person.name, "id": person.pilot_id, "person_type": formatted_type})

        elif person_type in ["ChiefCabinCrew", "RegularCabinCrew"]:
            person = CabinCrew.query.get(assignment.seater_id)
            # Format the person type by inserting a space
            formatted_type = person_type.replace("CabinCrew", " Cabin Crew")
            person_data.update({"name": person.name, "id": person.attendant_id, "person_type": formatted_type})

        elif person_type == "ChefCabinCrew":
            person = CabinCrew.query.get(assignment.seater_id)
            person_data.update({"name": person.name, "id": person.attendant_id, "person_type": "Chef"})

        data.append(person_data)

    return jsonify(data), 200

@flight_views.route('/<int:flight_id>/plane_view', methods=['GET'])
def plane_view(flight_id):
    # Check if the flight exists
    if not Flight.query.get(flight_id):
        return jsonify({"error": "Flight not found"}), 404

    # Fetch seat assignments for the specific flight
    assignments = FlightSeatAssignment.query.filter(FlightSeatAssignment.flight_id == flight_id).join(SeatMap, FlightSeatAssignment.seat_map_id == SeatMap.id).all()
    # print(assignments)
    data = []
    for assignment in assignments:
        seat_map = assignment.seat_map  # Access the joined SeatMap object
        person_type = assignment.seater_type
        seat_info = {
            "seat_row": seat_map.seat_row,  # Correctly access seat_row from the SeatMap object
            "seat_number": seat_map.seat_number,  # Correctly access seat_number from the SeatMap object
            "seat_type": seat_map.seat_type
        }

        if person_type == "Passenger":
            person = Passenger.query.get(assignment.seater_id)
            person_info = {
                "id": person.passenger_id,
                "person_type": person_type,
                "name": person.name,
                "parent_id": person.parent_id,
                "affiliated_passenger_ids": person.affiliated_passenger_ids,
            }

        elif person_type in ["SeniorPilot", "JuniorPilot", "TraineePilot"]:
            person = Pilot.query.get(assignment.seater_id)
            person_info = {
                "id": person.pilot_id,
                "person_type": person.seniority_level.capitalize() + " Pilot",
                "name": person.name,
                "seniority_level": person.seniority_level,
            }

        elif person_type in ["ChiefCabinCrew", "RegularCabinCrew", "ChefCabinCrew"]:
            person = CabinCrew.query.get(assignment.seater_id)
            print(person.attendant_id, person.name, person.attendant_type)
            crew_type = " Cabin Crew" if person_type != "ChefCabinCrew" else ""
            person_info = {
                "id": person.attendant_id,
                "person_type": person_type.replace("CabinCrew", crew_type),
                "name": person.name,
            }

        data.append({**seat_info, **person_info})

    return jsonify(data), 200

@flight_views.route('/<int:flight_id>/extended_view', methods=['GET'])
def extended_view(flight_id):
    # Check if the flight exists
    if not Flight.query.get(flight_id):
        return jsonify({"error": "Flight not found"}), 404

    # Fetch seat assignments for the specific flight
    assignments = FlightSeatAssignment.query.filter(FlightSeatAssignment.flight_id == flight_id).all()

    # Initialize data structures for each type of person
    flight_crew_data = []
    cabin_crew_data = []
    passenger_data = []

    for assignment in assignments:
        person_type = assignment.seater_type

        if "Pilot" in person_type:  # Assuming types like 'SeniorPilot', etc.
            person = Pilot.query.get(assignment.seater_id)
            person_info = {
                "id": person.pilot_id,
                "person_type": person.seniority_level.capitalize() + " Pilot",
                "name": person.name,
                "age": person.age,
                "gender": person.gender,
                "nationality": person.nationality,
                "known_languages": person.known_languages,
                "vehicle_type_id": person.vehicle_type_id,
                "allowed_range": person.allowed_range,
                "scheduled_flights": person.scheduled_flights
            }
            flight_crew_data.append(person_info)

        elif "Crew" in person_type:  # Types like 'ChiefCabinCrew', etc.
            person = CabinCrew.query.get(assignment.seater_id)
            crew_type = " Cabin Crew" if "CabinCrew" in person_type else ""
            person_info = {
                "id": person.attendant_id,
                "person_type": person_type.replace("CabinCrew", crew_type),
                "name": person.name,
                "age": person.age,
                "gender": person.gender,
                "nationality": person.nationality,
                "known_languages": person.known_languages,
                "vehicle_type_ids": person.vehicle_type_ids,
                "attendant_type": person.attendant_type,
                "dish_recipes": person.dish_recipes,
                "scheduled_flights": person.scheduled_flights,
            }
            cabin_crew_data.append(person_info)

        elif person_type == "Passenger":
            person = Passenger.query.get(assignment.seater_id)
            person_info = {
                "id": person.passenger_id,
                "person_type": person_type,
                "name": person.name,
                "age": person.age,
                "gender": person.gender,
                "nationality": person.nationality,
                "parent_id": person.parent_id,
                "affiliated_passenger_ids": person.affiliated_passenger_ids,
                "scheduled_flights": person.scheduled_flights
            }
            passenger_data.append(person_info)

    return jsonify([
        flight_crew_data,
        cabin_crew_data,
        passenger_data
    ]), 200