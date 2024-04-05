from math import radians, cos, sin, sqrt, atan2
from datetime import datetime, timedelta
import random
from models import db, Flight, AircraftType, Airport, Pilot, CabinCrew, Passenger, SeatMap, FlightSeatAssignment
import numpy as np

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def scheduleIsAvailable(start_time, end_time, person_type, id):
    scheduled_flights = person_type.query.get(id).scheduled_flights
    for flight_number in scheduled_flights:
        flight = Flight.query.get(flight_number)
        if flight.flight_time < end_time and flight.flight_time + timedelta(minutes = flight.duration) > start_time:
            return False
    return True

def find_available_pilots(flight_id, pilot_type, num_needed):
    flight_start_time = Flight.query.get(flight_id).flight_time
    flight_end_time = flight_start_time + timedelta(minutes = Flight.query.get(flight_id).duration)
    flight_distance = Flight.query.get(flight_id).distance
    vehicle_type_id = Flight.query.get(flight_id).vehicle_type_id

    unavailable_pilots = set()
    found_pilots = []
    while(len(found_pilots) != num_needed):
        pilot = Pilot.query.filter(Pilot.seniority_level == pilot_type, Pilot.vehicle_type_id == vehicle_type_id
        ).filter(Pilot.pilot_id.notin_(unavailable_pilots)
        ).order_by(db.func.random()).first()
        if pilot is None:
            return False
        if (pilot.allowed_range < flight_distance) or (not scheduleIsAvailable(flight_start_time, flight_end_time, "Pilot", "pilot_id")):
            unavailable_pilots.add(pilot.pilot_id)
        else:
          found_pilots.append(pilot.pilot_id)
    return found_pilots

def find_available_cabin_crew(flight_id, cabin_crew_type, num_needed):
    flight_start_time = Flight.query.get(flight_id).flight_time
    flight_end_time = flight_start_time + timedelta(minutes = Flight.query.get(flight_id).duration)
    flight_distance = Flight.query.get(flight_id).distance
    vehicle_type_id = Flight.query.get(flight_id).vehicle_type_id

    unavailable_cabin_crew = set()
    found_cabin_crew = []
    while(len(found_cabin_crew) != num_needed):
        cabin_crew = CabinCrew.query.filter(CabinCrew.attendant_type == cabin_crew_type, CabinCrew.vehicle_type_ids.contains(vehicle_type_id)
        ).filter(CabinCrew.attendant_id.notin_(unavailable_cabin_crew)
        ).order_by(db.func.random()).first()
        if cabin_crew is None:
            return "Error"
        if (not scheduleIsAvailable(flight_start_time, flight_end_time, "CabinCrew", "attendant_id")):
            unavailable_cabin_crew.add(cabin_crew.attendant_id)
        else:
          found_cabin_crew.append(cabin_crew.attendant_id)
    return found_cabin_crew

def find_available_passengers(flight_id, num_needed):
    flight_start_time = Flight.query.get(flight_id).flight_time
    flight_end_time = flight_start_time + timedelta(minutes = Flight.query.get(flight_id).duration)
    flight_distance = Flight.query.get(flight_id).distance

    unavailable_passengers = set()
    found_passengers = []
    while(len(found_passengers) != num_needed):
        passenger = Passenger.query.filter(Passenger.passenger_id.notin_(unavailable_passengers)
        ).order_by(db.func.random()).first()
        if passenger is None:
            return "Error"
        if (not scheduleIsAvailable(flight_start_time, flight_end_time, "Passenger", "passenger_id")):
            unavailable_passengers.add(passenger.passenger_id)
        else:
          found_passengers.append(passenger.passenger_id)
    return found_passengers
    

def seat_plan_auto(flight_number, vehicle_type_id):

    # Boeing 737 or Airbus A320
    if(vehicle_type_id == 1 or vehicle_type_id == 2):
        senior_pilot_num_needed = 1
        junior_pilot_num_needed = 1
        trainee_pilot_num_needed = random.randint(0, 2)
        chief_cabin_crew_num_needed = 2
        regular_cabin_crew_num_needed = random.randint(2, 4)
        chef_num_needed = random.randint(0, 2)
        passenger_num_needed = max(10, int(np.random.normal(70, 20)))
        if passenger_num_needed > 120:
            passenger_num_needed = 120

    # Boeing 777
    elif(vehicle_type_id == 3):
        senior_pilot_num_needed = random.randint(1, 2)
        junior_pilot_num_needed = random.randint(1, 2)
        trainee_pilot_num_needed = random.randint(1, 2)
        chief_cabin_crew_num_needed = 4
        regular_cabin_crew_num_needed = random.randint(6, 10)
        chef_num_needed = random.randint(0, 2)
        passenger_num_needed = max(20, int(np.random.normal(100, 30)))
        if passenger_num_needed > 160:
            passenger_num_needed = 160

    senior_pilots = find_available_pilots(flight_number, "senior", senior_pilot_num_needed)
    if senior_pilots == "Error":
        
        return "Not enough available senior pilots"
    junior_pilots = find_available_pilots(flight_number, "junior", junior_pilot_num_needed)
    if junior_pilots == "Error":
        
        return "Not enough available junior pilots"
    trainee_pilots = find_available_pilots(flight_number, "trainee", trainee_pilot_num_needed)
    if trainee_pilots == "Error":
        return "Not enough available trainee pilots"
    
    chief_cabin_crews = find_available_cabin_crew(flight_number, "chief", chief_cabin_crew_num_needed)
    if chief_cabin_crews == "Error":
        return "Not enough available senior cabin crew"
    
    regular_cabin_crews = find_available_cabin_crew(flight_number, "regular", regular_cabin_crew_num_needed)
    if regular_cabin_crews == "Error":
        return "Not enough available regular cabin crew"
    
    if(chef_num_needed > 0):
        chefs = find_available_cabin_crew(flight_number, "chef", chef_num_needed)
        if chefs == "Error":
            return "Not enough available chefs"
        
    passengers = find_available_passengers(flight_number, passenger_num_needed)
    if passengers == "Error":
        return "Not enough available passengers"
    
    
def assign_seats(senior_pilots, junior_pilots, trainee_pilots, chief_cabin_crews, regular_cabin_crews, chefs, passengers, flight_number, vehicle_type_id):
    
    if(vehicle_type_id == 1 or vehicle_type_id == 2):
        
        index = SeatMap.query.filter(SeatMap.aircraft_type_id == vehicle_type_id, SeatMap.seater_type == "pilot").first().id
        db.session.add(FlightSeatAssignment(
            flight_number=flight_number,
            seat_map_id=index,
            seater_type="pilot",
            seater_id=senior_pilots[0].pilot_id
        ))
        index += 1
        db.session.add(FlightSeatAssignment(
            flight_number=flight_number,
            seat_map_id=index,
            seater_type="pilot",
            seater_id=junior_pilots[0].pilot_id
        ))
        index += 1
        for pilot in trainee_pilots:
            db.session.add(FlightSeatAssignment(
                flight_number=flight_number,
                seat_map_id=index,
                seater_type="pilot",
                seater_id=pilot
            ))
            index += 1
        index = SeatMap.query.filter(SeatMap.aircraft_type_id == vehicle_type_id, SeatMap.seater_type == "cabin_crew").first().id
        for cabin_crew in chief_cabin_crews:
            db.session.add(FlightSeatAssignment(
                flight_number=flight_number,
                seat_map_id=index,
                seater_type="cabin_crew",
                seater_id=cabin_crew
            ))
            index += 1
        
    

        
    
        
    
        
    


            
                
        
    
