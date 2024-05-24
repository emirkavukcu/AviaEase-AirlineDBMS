from models import db, Flight, Pilot, CabinCrew, Passenger, SeatMap, FlightSeatAssignment
from .availability_service import find_available_pilots, find_available_cabin_crew, find_available_passengers  
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import flag_modified
import numpy as np
import random


def seat_plan_auto(flight_number, vehicle_type_id):
    # Default values to avoid UnboundLocalError
    senior_pilot_num_needed = 0
    junior_pilot_num_needed = 0
    trainee_pilot_num_needed = 0
    chief_cabin_crew_num_needed = 0
    regular_cabin_crew_num_needed = 0
    chef_num_needed = 0
    passenger_num_needed = 0

    # Boeing 737 or Airbus A320
    if vehicle_type_id == 1 or vehicle_type_id == 2:
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
    elif vehicle_type_id == 3:
        senior_pilot_num_needed = random.randint(1, 2)
        junior_pilot_num_needed = random.randint(1, 2)
        trainee_pilot_num_needed = random.randint(1, 2)
        chief_cabin_crew_num_needed = 4
        regular_cabin_crew_num_needed = random.randint(6, 10)
        chef_num_needed = random.randint(0, 2)
        passenger_num_needed = max(20, int(np.random.normal(100, 30)))
        if passenger_num_needed > 160:
            passenger_num_needed = 160

    # Handle unexpected vehicle_type_id
    else:
        return "Invalid vehicle type ID"

    senior_pilots = find_available_pilots(flight_number, "senior", senior_pilot_num_needed)
    if senior_pilots == "Error":
        return "Not enough available senior pilots"

    junior_pilots = find_available_pilots(flight_number, "junior", junior_pilot_num_needed)
    if junior_pilots == "Error":
        return "Not enough available junior pilots"

    trainee_pilots = find_available_pilots(flight_number, "trainee", trainee_pilot_num_needed)
    if trainee_pilots == "Error":
        trainee_pilots = []

    chief_cabin_crews = find_available_cabin_crew(flight_number, "chief", chief_cabin_crew_num_needed)
    if chief_cabin_crews == "Error":
        return "Not enough available senior cabin crew"

    regular_cabin_crews = find_available_cabin_crew(flight_number, "regular", regular_cabin_crew_num_needed)
    if regular_cabin_crews == "Error":
        return "Not enough available regular cabin crew"

    chefs = []
    if chef_num_needed > 0:
        chefs = find_available_cabin_crew(flight_number, "chef", chef_num_needed)

    passengers = find_available_passengers(flight_number, passenger_num_needed)
    if passengers == "Error":
        return "Not enough available passengers"

    result = assign_seats(senior_pilots, junior_pilots, trainee_pilots, chief_cabin_crews, regular_cabin_crews, chefs,
                          passengers, flight_number, vehicle_type_id)
    return result


def assign_seats(senior_pilots, junior_pilots, trainee_pilots, chief_cabin_crews, regular_cabin_crews, chefs, passengers, flight_number, vehicle_type_id):
    
    if(vehicle_type_id == 1 or vehicle_type_id == 2):     
        seniorPilotIdx = SeatMap.query.filter(SeatMap.aircraft_type_id == vehicle_type_id, SeatMap.seat_type == "pilot").first().id
        juniorPilotIdx = seniorPilotIdx + 1
        traineePilotIdx = juniorPilotIdx + 1
        chiefCabinCrewIdx = traineePilotIdx + 2
        regularCabinCrewIdx = chiefCabinCrewIdx + 2
        chefIdx = regularCabinCrewIdx + 8
   
    elif(vehicle_type_id == 3):
        seniorPilotIdx = SeatMap.query.filter(SeatMap.aircraft_type_id == vehicle_type_id, SeatMap.seat_type == "pilot").first().id
        juniorPilotIdx = seniorPilotIdx + 2
        traineePilotIdx = juniorPilotIdx + 2
        chiefCabinCrewIdx = traineePilotIdx + 2
        regularCabinCrewIdx = chiefCabinCrewIdx + 4
        chefIdx = regularCabinCrewIdx + 10
        
    for i in range(len(senior_pilots)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= seniorPilotIdx + i, seater_id=senior_pilots[i], seater_type="SeniorPilot"))
        pilot = Pilot.query.get(senior_pilots[i])
        pilot.scheduled_flights.append(flight_number)
        flag_modified(pilot, 'scheduled_flights')

    for i in range(len(junior_pilots)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= juniorPilotIdx + i, seater_id=junior_pilots[i], seater_type="JuniorPilot"))
        pilot = Pilot.query.get(junior_pilots[i])
        pilot.scheduled_flights.append(flight_number)
        flag_modified(pilot, 'scheduled_flights')

    for i in range(len(trainee_pilots)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= traineePilotIdx + i, seater_id=trainee_pilots[i], seater_type="TraineePilot"))
        pilot = Pilot.query.get(trainee_pilots[i])
        pilot.scheduled_flights.append(flight_number)
        flag_modified(pilot, 'scheduled_flights')

    for i in range(len(chief_cabin_crews)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= chiefCabinCrewIdx + i, seater_id=chief_cabin_crews[i], seater_type="ChiefCabinCrew"))
        crew = CabinCrew.query.get(chief_cabin_crews[i])
        crew.scheduled_flights.append(flight_number)
        flag_modified(crew, 'scheduled_flights')

    for i in range(len(regular_cabin_crews)):
        db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= regularCabinCrewIdx + i, seater_id=regular_cabin_crews[i], seater_type="RegularCabinCrew"))
        crew = CabinCrew.query.get(regular_cabin_crews[i])
        crew.scheduled_flights.append(flight_number)
        flag_modified(crew, 'scheduled_flights')
   
    flight = Flight.query.get(flight_number)
    if not flight:
        return "Flight not found"
    
    if chefs:
        menu_updated = False
        for i, chef_id in enumerate(chefs):
            db.session.add(FlightSeatAssignment(flight_id=flight_number, seat_map_id= chefIdx + i, seater_id=chef_id, seater_type="ChefCabinCrew"))
            current_chef = CabinCrew.query.get(chef_id)
            current_chef.scheduled_flights.append(flight_number)
            flag_modified(current_chef, 'scheduled_flights')
            unique_dishes = [dish for dish in current_chef.dish_recipes if dish not in flight.flight_menu]
            if unique_dishes:
                random_dish = random.choice(unique_dishes)
                flight.flight_menu.append(random_dish)  # Add unique dish to the flight menu  
                menu_updated = True
        if menu_updated:
            flag_modified(flight, "flight_menu")
                
    result = assign_seats_for_passengers(passengers, flight_number, vehicle_type_id)
    return result

def assign_seats_for_passengers(passenger_ids, flight_number, vehicle_type_id):
    total_seats = 122 if vehicle_type_id in [1, 2] else 160
    seat_maps = SeatMap.query.filter(
        SeatMap.aircraft_type_id == vehicle_type_id,
        SeatMap.seat_type.in_(['business', 'economy'])
    ).order_by(SeatMap.id).all()

    seat_groups = {}
    for seat in seat_maps:
        if seat.seat_group not in seat_groups:
            seat_groups[seat.seat_group] = []
        seat_groups[seat.seat_group].append(seat.id)

    shuffled_seat_groups = list(seat_groups.items())
    random.shuffle(shuffled_seat_groups)

    passengers = {p.passenger_id: p for p in Passenger.query.filter(Passenger.passenger_id.in_(passenger_ids)).all()}
    assigned_seats = {}
    assigned_passengers = set()

    for passenger_id in passenger_ids:
        passenger = passengers.get(passenger_id)
        if passenger_id in assigned_passengers:
            continue

        affiliated_ids = passenger.affiliated_passenger_ids or []
        affiliated_passengers = [passengers.get(aff_id) for aff_id in affiliated_ids if aff_id in passengers]

        for group, seats in shuffled_seat_groups:
            if all(ap_id not in assigned_passengers for ap_id in affiliated_ids) and len(seats) >= len(affiliated_passengers) + 1:
                assigned_seats[passenger_id] = seats.pop(0)
                assigned_passengers.add(passenger_id)
                passenger.scheduled_flights.append(flight_number)
                flag_modified(passenger, 'scheduled_flights')
                for affiliated_passenger in affiliated_passengers:
                    if affiliated_passenger:
                        assigned_seats[affiliated_passenger.passenger_id] = seats.pop(0)
                        assigned_passengers.add(affiliated_passenger.passenger_id)
                        affiliated_passenger.scheduled_flights.append(flight_number)
                        flag_modified(affiliated_passenger, 'scheduled_flights')
                break
            else:
                if seats and passenger_id not in assigned_passengers:
                    assigned_seats[passenger_id] = seats.pop(0)
                    assigned_passengers.add(passenger_id)
                    passenger.scheduled_flights.append(flight_number)
                    flag_modified(passenger, 'scheduled_flights')
                    break

    try:
        for passenger_id, seat_id in assigned_seats.items():
            db.session.add(FlightSeatAssignment(
                flight_id=flight_number,
                seat_map_id=seat_id,
                seater_id=passenger_id,
                seater_type='Passenger'
            ))
        db.session.commit()
        return "Seats assigned successfully"
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Database error during seat assignment: {str(e)}"