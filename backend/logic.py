from math import radians, cos, sin, sqrt, atan2
from datetime import datetime, timedelta
import random
from models import db, Flight, AircraftType, Airport, Pilot, CabinCrew, Passenger, SeatMap, FlightSeatAssignment
import numpy as np
import random
from sqlalchemy.exc import SQLAlchemyError

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
            return "Error"
        if (pilot.allowed_range < flight_distance) or (not scheduleIsAvailable(flight_start_time, flight_end_time, "Pilot", "pilot_id")):
            unavailable_pilots.add(pilot.pilot_id)
        else:
          found_pilots.append(pilot.pilot_id)
    return found_pilots

def find_available_cabin_crew(flight_id, cabin_crew_type, num_needed):
    flight_start_time = Flight.query.get(flight_id).flight_time
    flight_end_time = flight_start_time + timedelta(minutes = Flight.query.get(flight_id).duration)
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
        regular_cabin_crew_num_needed = random.randint(4, 8)
        chef_num_needed = random.randint(0, 2)
        passenger_num_needed = max(10, int(np.random.normal(70, 20)))
        if passenger_num_needed > 122:
            passenger_num_needed = 122

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

    assign_seats(senior_pilots, junior_pilots, trainee_pilots, chief_cabin_crews, regular_cabin_crews, chefs, passengers, flight_number, vehicle_type_id)    
    
def assign_seats(senior_pilots, junior_pilots, trainee_pilots, chief_cabin_crews, regular_cabin_crews, chefs, passengers, flight_number, vehicle_type_id):
    
    if(vehicle_type_id == 1 or vehicle_type_id == 2):     
        seniorPilotIdx = SeatMap.query.filter(SeatMap.aircraft_type_id == vehicle_type_id, SeatMap.seater_type == "pilot").first().id
        juniorPilotIdx = seniorPilotIdx + 1
        traineePilotIdx = juniorPilotIdx + 1
        chiefCabinCrewIdx = traineePilotIdx + 2
        regularCabinCrewIdx = chiefCabinCrewIdx + 2
        chefIdx = regularCabinCrewIdx + 8
   
    elif(vehicle_type_id == 3):
        seniorPilotIdx = SeatMap.query.filter(SeatMap.aircraft_type_id == vehicle_type_id, SeatMap.seater_type == "pilot").first().id
        juniorPilotIdx = seniorPilotIdx + 2
        traineePilotIdx = juniorPilotIdx + 2
        chiefCabinCrewIdx = traineePilotIdx + 2
        regularCabinCrewIdx = chiefCabinCrewIdx + 4
        chefIdx = regularCabinCrewIdx + 10
        
    for i in range(len(senior_pilots)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= seniorPilotIdx + i, seater_id=senior_pilots[i], seater_type="SeniorPilot"))
    for i in range(len(junior_pilots)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= juniorPilotIdx + i, seater_id=junior_pilots[i], seater_type="JuniorPilot"))
    for i in range(len(trainee_pilots)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= traineePilotIdx + i, seater_id=trainee_pilots[i], seater_type="TraineePilot"))
    for i in range(len(chief_cabin_crews)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= chiefCabinCrewIdx + i, seater_id=chief_cabin_crews[i], seater_type="ChiefCabinCrew"))
    for i in range(len(regular_cabin_crews)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= regularCabinCrewIdx + i, seater_id=regular_cabin_crews[i], seater_type="RegularCabinCrew"))
    if(len(chefs) > 0):
        for i in range(len(chefs)):
            db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= chefIdx + i, seater_id=chefs[i], seater_type="ChefCabinCrew"))
    
    assign_seats_for_passengers(passengers, flight_number, vehicle_type_id)

def assign_seats_for_passengers(passengers, flight_number, vehicle_type_id):
  # Determine total passenger seats based on the aircraft type
  total_seats = 122 if vehicle_type_id in [1, 2] else 160

  # Fetch seat maps for passenger seats
  seat_maps = SeatMap.query.filter(
    SeatMap.aircraft_type_id == vehicle_type_id,
    SeatMap.seat_type.in_(['business', 'economy'])
  ).order_by(SeatMap.id).all()

  # Create a map of seat groups to their available seat ids
  seat_groups = {}
  for seat in seat_maps:
    if seat.seat_group not in seat_groups:
      seat_groups[seat.seat_group] = []
    seat_groups[seat.seat_group].append(seat.id)

  # Shuffle seat groups to randomize seat assignment
  shuffled_seat_groups = list(seat_groups.items())
  random.shuffle(shuffled_seat_groups)

  for group in shuffled_seat_groups:
    random.shuffle(group[1])  # Shuffle the seat IDs within each group

  # Prepare to track assigned seats and passengers
  assigned_seats = {}
  assigned_passengers = set()

  # Assign seats
  for passenger in passengers:
    # Skip if passenger has already been assigned a seat
    if passenger.passenger_id in assigned_passengers:
      continue

    affiliated_ids = passenger.affiliated_passenger_ids or []
    affiliated_passengers = [p for p in passengers if p.passenger_id in affiliated_ids]

    # Attempt to seat affiliated passengers together
    for group, seats in shuffled_seat_groups:
      # Check if the group can accommodate this passenger and all their affiliates
      if all(p.passenger_id not in assigned_passengers for p in affiliated_passengers) and len(seats) >= len(affiliated_passengers) + 1:
        # Assign seats to the main passenger and their affiliates
        assigned_seats[passenger.passenger_id] = seats.pop(0)
        assigned_passengers.add(passenger.passenger_id)
        for affiliated_passenger in affiliated_passengers:
          assigned_seats[affiliated_passenger.passenger_id] = seats.pop(0)
          assigned_passengers.add(affiliated_passenger.passenger_id)
        break
    else:
      # If no suitable group found, assign the next available seat
      for group, seats in shuffled_seat_groups:
        if seats and passenger.passenger_id not in assigned_passengers:
          assigned_seats[passenger.passenger_id] = seats.pop(0)
          assigned_passengers.add(passenger.passenger_id)
          break

  # Store the seat assignments in the database
    try:
        for passenger_id, seat_id in assigned_seats.items():
            db.session.add(FlightSeatAssignment(
                flight_id=flight_number,
                seat_map_id=seat_id,
                seater_id=passenger_id,
                seater_type='Passenger'
            ))
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error during seat assignment: {str(e)}")
        return False






        
        
    

        
    
        
    
        
    


            
                
        
    
