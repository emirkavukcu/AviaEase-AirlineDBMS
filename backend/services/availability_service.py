from datetime import  timedelta
from models import db, Flight, Pilot, CabinCrew, Passenger

def scheduleIsAvailable(start_time, end_time, person_type, id):
    scheduled_flights = person_type.query.get(id).scheduled_flights
    for flight_number in scheduled_flights:
        flight = Flight.query.get(flight_number)
        if flight.date_time < end_time and flight.date_time + timedelta(minutes = flight.duration) > start_time:
            return False
    return True

def find_available_pilots(flight_id, pilot_type, num_needed):
    flight_start_time = Flight.query.get(flight_id).date_time
    flight_end_time = flight_start_time + timedelta(minutes = Flight.query.get(flight_id).duration)
    flight_distance = Flight.query.get(flight_id).distance
    vehicle_type_id = Flight.query.get(flight_id).aircraft_type_id

    unavailable_pilots = set()
    found_pilots = []
    while(len(found_pilots) != num_needed):
        pilot = Pilot.query.filter(Pilot.seniority_level == pilot_type, Pilot.vehicle_type_id == vehicle_type_id
        ).filter(Pilot.pilot_id.notin_(unavailable_pilots)
        ).order_by(db.func.random()).first()
        if pilot is None:
            return "Error"
        if (pilot.allowed_range < flight_distance) or (not scheduleIsAvailable(flight_start_time, flight_end_time, Pilot, pilot.pilot_id)):
            unavailable_pilots.add(pilot.pilot_id)
        else:
          found_pilots.append(pilot.pilot_id)
    return found_pilots

def find_available_cabin_crew(flight_id, cabin_crew_type, num_needed):
    flight_start_time = Flight.query.get(flight_id).date_time
    flight_end_time = flight_start_time + timedelta(minutes=Flight.query.get(flight_id).duration)
    vehicle_type_id = Flight.query.get(flight_id).aircraft_type_id

    unavailable_cabin_crew = set()
    found_cabin_crew = []
    while(len(found_cabin_crew) != num_needed):
        cabin_crew = CabinCrew.query.filter(
            CabinCrew.attendant_type == cabin_crew_type,
            CabinCrew.vehicle_type_ids.op('@>')([vehicle_type_id])
        ).filter(CabinCrew.attendant_id.notin_(unavailable_cabin_crew)
        ).order_by(db.func.random()).first()

        if cabin_crew is None:
            return "Error"
        if (not scheduleIsAvailable(flight_start_time, flight_end_time, CabinCrew, cabin_crew.attendant_id)):
            unavailable_cabin_crew.add(cabin_crew.attendant_id)
        else:
          found_cabin_crew.append(cabin_crew.attendant_id)
    return found_cabin_crew

def find_available_passengers(flight_id, num_needed):
    flight_start_time = Flight.query.get(flight_id).date_time
    flight_end_time = flight_start_time + timedelta(minutes = Flight.query.get(flight_id).duration)

    unavailable_passengers = set()
    found_passengers = []
    while(len(found_passengers) != num_needed):
        passenger = Passenger.query.filter(Passenger.passenger_id.notin_(unavailable_passengers)
        ).order_by(db.func.random()).first()
        if passenger is None:
            return "Error"
        if (not scheduleIsAvailable(flight_start_time, flight_end_time, Passenger, passenger.passenger_id)):
            unavailable_passengers.add(passenger.passenger_id)
        else:
          found_passengers.append(passenger.passenger_id)
    return found_passengers