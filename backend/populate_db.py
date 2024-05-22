from models import db, Flight, AircraftType, SeatMap, Airport, Pilot, CabinCrew, Passenger, FlightSeatAssignment
from faker import Faker
import random
import numpy as np
import airportsdata
from sqlalchemy.orm.attributes import flag_modified
from services import seat_plan_auto, calculate_distance
from datetime import datetime, timedelta

nationality_locale_mapping = {
    'Chinese': ('zh_CN', 'Mandarin'),
    'Indian': ('hi_IN', 'Hindi'),
    'American': ('en_US', 'English'),
    'Indonesian': ('id_ID', 'Indonesian'),
    'Brazilian': ('pt_BR', 'Portuguese'),
    'Pakistani': ('ur_PK', 'Urdu'),
    'Nigerian': ('en_NG', 'English'),  
    'Bangladeshi': ('bn_BD', 'Bengali'),
    'Russian': ('ru_RU', 'Russian'),
    'Japanese': ('ja_JP', 'Japanese'),
    'Mexican': ('es_MX', 'Spanish'),
    'Filipino': ('tl_PH', 'Filipino'),  
    'Egyptian': ('ar_EG', 'Arabic'),
    'Vietnamese': ('vi_VN', 'Vietnamese'),
    'Turkish': ('tr_TR', 'Turkish'),
    'Iranian': ('fa_IR', 'Persian'),
    'German': ('de_DE', 'German'),
    'Sweden': ('sv_SE', 'Swedish'),
    'French': ('fr_FR', 'French'),
    'Thai': ('th_TH', 'Thai'),
    'British': ('en_GB', 'English'),
    'Italian': ('it_IT', 'Italian'),
    'South Korean': ('ko_KR', 'Korean'),
    'Colombian': ('es_CO', 'Spanish'),
    'Spanish': ('es_ES', 'Spanish'),
    'Ukrainian': ('uk_UA', 'Ukrainian'),
    'Kenyan': ('sw_KE', 'Swahili'),  
    'Argentine': ('es_AR', 'Spanish'),
}

def populate_seatmaps():
        
    # Populate Boeing 737 and Airbus A320 seat map
    for i in range(1,3):
        for k in range(1, 5):  # 4 Pilot seats
            db.session.add(SeatMap(aircraft_type_id = i, seat_row="PL", seat_number=k, seat_type="pilot"))
        for k in range(1, 13):  # 12 Crew seats
            db.session.add(SeatMap(aircraft_type_id = i, seat_row="CR", seat_number=k, seat_type="crew"))

        seat_group_idx = 1

        # 32 Businnes seats
        for row in 'ABCDEFGH':  
            for num in range(1, 3):  
                db.session.add(SeatMap(aircraft_type_id = i, seat_row=row, seat_number=num, seat_type="business", seat_group= seat_group_idx, seat_group_size=2))
            seat_group_idx += 1
            for num in range(3, 5):  
                db.session.add(SeatMap(aircraft_type_id = i, seat_row=row, seat_number=num, seat_type="business", seat_group= seat_group_idx, seat_group_size=2))
            seat_group_idx += 1

        # 90 Economy seats
        for row in 'ABCDEFGHIJKLMNO':  
            for num in range(1, 4):  
                db.session.add(SeatMap(aircraft_type_id = i, seat_row=row, seat_number=num, seat_type="economy", seat_group= seat_group_idx, seat_group_size=3))
            seat_group_idx += 1
            for num in range(4, 7):  
                db.session.add(SeatMap(aircraft_type_id = i, seat_row=row, seat_number=num, seat_type="economy", seat_group= seat_group_idx, seat_group_size=3))
            seat_group_idx += 1

        db.session.commit()

    # Populate Boeing 777 seat map
    for k in range(1, 7):  # 6 Pilot seats
        db.session.add(SeatMap(aircraft_type_id = 3, seat_row="PL", seat_number=k, seat_type="pilot"))
        
    for k in range(1, 17):  # 16 Crew seats
        db.session.add(SeatMap(aircraft_type_id = 3, seat_row="CR", seat_number=k, seat_type="crew"))
    
    seat_group_idx = 1
    # 40 Businnes seats
    for row in 'ABCDEFGHIJ':  
        for num in range(1, 3):  
            db.session.add(SeatMap(aircraft_type_id = 3, seat_row=row, seat_number=num, seat_type="business", seat_group= seat_group_idx, seat_group_size=2))
        seat_group_idx += 1
        for num in range(3, 5):  
            db.session.add(SeatMap(aircraft_type_id = 3, seat_row=row, seat_number=num, seat_type="business", seat_group= seat_group_idx, seat_group_size=2))
        seat_group_idx += 1

    # 120 Economy seats
    for row in 'ABCDEFGHIJKLMNO':  
        for num in range(1, 3):  
            db.session.add(SeatMap(aircraft_type_id = 3, seat_row=row, seat_number=num, seat_type="economy", seat_group= seat_group_idx, seat_group_size=2))
        seat_group_idx += 1
        for num in range(3, 7):  
            db.session.add(SeatMap(aircraft_type_id = 3, seat_row=row, seat_number=num, seat_type="economy", seat_group= seat_group_idx, seat_group_size=4))
        seat_group_idx += 1
        for num in range(7, 9):  
            db.session.add(SeatMap(aircraft_type_id = 3, seat_row=row, seat_number=num, seat_type="economy", seat_group= seat_group_idx, seat_group_size= 2))


    db.session.commit()

def populate_aircraft_types():
    db.session.add(AircraftType(
        name="Boeing 737",
        seat_count=138,
        crew_limit=16,  
        passenger_limit=122,  
        standard_menu = [
            'Chicken Caesar Salad',  
            'Vegetarian Pasta Primavera',  
            'Beef Stroganoff with Rice',  
            'Salmon with Lemon Butter Sauce',  
        ]
    ))

    db.session.add(AircraftType(
        name="Airbus A320",
        seat_count=138,
        crew_limit=16,  
        passenger_limit=122,  
        standard_menu = [
            'Roasted Chicken with Vegetables',  
            'Vegan Lentil and Mushroom Stew',  
            'Grilled Shrimp over Saffron Rice',  
            'Mixed Nut Yogurt Parfait',  
        ]
    ))

    db.session.add(AircraftType(
        name="Boeing 777",
        seat_count=182,
        crew_limit=22,  
        passenger_limit=160,  
        standard_menu = [
            'Stuffed Chicken Breast', 
            'Butternut Squash Risotto',  
            'Asian Beef Salad ',  
            'Chickpea andPotato Curry',  
            'Glazed Salmon with Broccoli',  
            'Chocolate Mousse', 
        ]
    ))
    
    db.session.commit()

def populate_pilots(n):
    fake = Faker()
    for _ in range(n):
        nationality = random.choice(list(nationality_locale_mapping.keys()))
        gender = random.choice(['male', 'female'])
        if(gender == 'male'):
            name = fake.name_male()
        else:
            name = fake.name_female()
        # Generate age using a normal distribution centered at 40
        age = max(22, int(np.random.normal(40, 10)))
        known_languages = ['English']
        if(nationality not in ['American', 'British', 'Nigerian']):
            known_languages.append(nationality_locale_mapping[nationality][1])
        vehicle_type_id = random.randint(1, 3)
        
        if age < 30:
            seniority_level = 'trainee'
            allowed_range = 2000
        else:
            seniority_level = random.choices(['junior', 'senior'], weights=(70, 30), k=1)[0]
            allowed_range = random.choice([5000, 10000, 15000, 20000])

        pilot = Pilot(
            name=name,
            age=age,
            gender=gender,
            nationality=nationality,
            known_languages=known_languages,
            vehicle_type_id=vehicle_type_id,
            allowed_range=allowed_range,
            seniority_level=seniority_level,
            scheduled_flights=[]  # Initialize to ensure it's not null
        )
        
        db.session.add(pilot)
    
    db.session.commit()

def populate_cabin_crew(n):
    dishes = [
    'Grilled Salmon with Dill Sauce',
    'Roasted Chicken with Rosemary',
    'Vegetable Lasagna',
    'Beef Bourguignon',
    'Thai Green Curry',
    'Mushroom Risotto',
    'Quinoa Salad with Avocado',
    'Pulled Pork Tacos',
    'Shrimp Paella', 
    'Vegan Burger'
    ]
    fake = Faker()
    for _ in range(n):
        nationality = random.choice(list(nationality_locale_mapping.keys()))
        age = max(18, int(np.random.normal(35, 15))) 
        gender = random.choice(['male', 'female'])
        if(gender == 'male'):
            name = fake.name_male()
        else:
            name = fake.name_female()
        attendant_type = random.choices(['chief', 'regular', 'chef'], weights=(20, 60, 20), k=1)[0]
        known_languages = ['English']
        if(nationality != 'American'):
            known_languages.append(nationality_locale_mapping[nationality][1])
        vehicle_type_ids = random.sample(range(1, 4), random.randint(1, 3)) 
        dish_recipes = None
        if attendant_type == 'chef':
            dish_recipes = random.sample(dishes, random.randint(2, 4))

        cabin_crew_member = CabinCrew(
            name=name,
            age=age,
            gender=gender,
            nationality=nationality,
            known_languages=known_languages,
            attendant_type=attendant_type,
            vehicle_type_ids=vehicle_type_ids,
            dish_recipes=dish_recipes,
            scheduled_flights=[]  # Initialize to ensure it's not null
        )
        
        db.session.add(cabin_crew_member)
    
    db.session.commit()

def populate_passengers(n):
    passengers = []
    fake = Faker()
    # Create all passengers
    for _ in range(n):
        age = random.randint(0, 90)  # Assume passenger age range is 0 to 90
        nationality = random.choice(list(nationality_locale_mapping.keys()))
        gender=random.choice(['male', 'female']),
        if(gender == 'male'):
            name = fake.name_male()
        else:
            name = fake.name_female()
        passenger = Passenger(
            name=name,
            nationality=nationality,
            gender=gender,
            age=age,
            parent_id=None,  # Will be updated for infants if applicable
            affiliated_passenger_ids=[],  # Initialize to ensure it's not null
            scheduled_flights=[]  # Initialize to ensure it's not null
        )
        passengers.append(passenger)
        db.session.add(passenger)

    db.session.commit()

    # Assign parents to infants (consider age > 20 for parents)
    infant_passengers = [p for p in passengers if p.age <= 2]
    adult_passengers = [p for p in passengers if p.age > 20]
    for infant in infant_passengers:
        if adult_passengers:
            infant.parent_id = random.choice(adult_passengers).passenger_id

    # Implement affiliations ensuring no passenger is affiliated with more than one group
    affiliated = set()  # Keep track of passengers who are already affiliated
    potential_affiliates = [p for p in passengers if p.age > 2 and p.passenger_id is not None]  # Exclude infants from affiliations

    # Assign 20% of passengers to groups of 2-3 passengers
    while len(affiliated) < int(0.2 * n) and potential_affiliates:
        primary = random.choice(potential_affiliates)
        potential_affiliates.remove(primary)
        if primary in affiliated:
            continue  # Skip if already affiliated

        num_affiliates = random.randint(1, 2)
        group = random.sample([p for p in potential_affiliates if p not in affiliated], k=num_affiliates)

        # Update affiliations
        primary.affiliated_passenger_ids = primary.affiliated_passenger_ids + [p.passenger_id for p in group]
        flag_modified(primary, "affiliated_passenger_ids")  # Mark as modified
        for other in group:
            other.affiliated_passenger_ids = other.affiliated_passenger_ids + [primary.passenger_id] + [another.passenger_id for another in group if another != other]
            flag_modified(other, "affiliated_passenger_ids")  # Mark as modified
            affiliated.add(other)

        affiliated.add(primary)

    db.session.commit()


def populate_airports():
    # Load all airports data with IATA codes
    all_airports = airportsdata.load('IATA')
    
    for code, details in all_airports.items():
        if 'iata' in details and details['iata'] and 'lat' in details and 'lon' in details:
            # Create a new Airport instance
            new_airport = Airport(
                airport_code=details['iata'],
                name=details.get('name', ''),
                city=details.get('city', ''),
                country=details.get('country', ''),
                latitude=details.get('lat', 0),
                longitude=details.get('lon', 0)
            )
            db.session.add(new_airport)
    
    db.session.commit()

def populate_flights_with_rosters(start_date, end_date, num_flights):
    all_airports = Airport.query.all()
    if len(all_airports) < 2:
        return "Not enough airports to create flights."

    for _ in range(num_flights):
        source_airport = random.choice(all_airports)
        destination_airport = random.choice([airport for airport in all_airports if airport != source_airport])
        vehicle_type_id = random.randint(1, 3)  # Assuming these IDs correspond to different aircraft types

        # Calculate distance and duration
        distance = calculate_distance(
            source_airport.longitude, source_airport.latitude,
            destination_airport.longitude, destination_airport.latitude
        )
        duration = distance / 15

        # Retrieve the flight menu from the aircraft type
        aircraft_type = AircraftType.query.get(vehicle_type_id)
        if not aircraft_type:
            return f"Invalid vehicle type ID {vehicle_type_id}"

        # Generate a random datetime between the start_date and end_date
        time_between_dates = end_date - start_date
        random_seconds = random.randrange(time_between_dates.total_seconds())
        flight_date = start_date + timedelta(seconds=random_seconds)
        flight_date = flight_date.replace(hour=random.randint(0, 23), minute=0, second=0)

        # Create the flight
        flight = Flight(
            airline_code="AE",
            date_time=flight_date,
            duration=int(duration),
            distance=int(distance),
            source_airport=source_airport.airport_code,
            destination_airport=destination_airport.airport_code,
            aircraft_type_id=vehicle_type_id,
            flight_menu=aircraft_type.standard_menu.copy()
        )
        db.session.add(flight)
        db.session.flush()  # Flush to get the flight_number generated
        
        # Auto generate seat plan for this flight
        result = seat_plan_auto(flight.flight_number, vehicle_type_id)
        if result != "Seats assigned successfully":
            db.session.rollback()  # Rollback if seat assignment fails
            continue

        db.session.commit()  # Commit after each flight and its seat assignments are successfully processed

    return "Flights with rosters populated successfully."