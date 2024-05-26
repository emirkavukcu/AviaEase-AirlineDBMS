from flask import Blueprint, request, jsonify
from models import CabinCrew, db
import random
from flask_jwt_extended import jwt_required

cabin_crew = Blueprint('cabin_crew', __name__)

@cabin_crew.route('/cabin-crew', methods=['GET'])
@jwt_required()
def get_crew_members():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Filtering parameters
    attendant_id = request.args.get('attendant_id', type=int)
    name = request.args.get('name', type=str)
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    gender = request.args.get('gender', type=str)
    nationality = request.args.get('nationality', type=str)
    attendant_type = request.args.get('attendant_type', type=str)
    vehicle_type_ids = request.args.getlist('vehicle_type_ids', type=int)  # Assumes array input handling

    # Building the query
    query = CabinCrew.query

    if attendant_id:
        query = query.filter(CabinCrew.attendant_id == attendant_id)
    if name:
        query = query.filter(CabinCrew.name.ilike(f'%{name}%'))
    if min_age:
        query = query.filter(CabinCrew.age >= min_age)
    if max_age:
        query = query.filter(CabinCrew.age <= max_age)
    if gender:
        query = query.filter(CabinCrew.gender.ilike(gender))
    if nationality:
        query = query.filter(CabinCrew.nationality.ilike(f'%{nationality}%'))
    if attendant_type:
        query = query.filter(CabinCrew.attendant_type.ilike(attendant_type))
    if vehicle_type_ids:
      for vehicle_type_id in vehicle_type_ids:
        query = query.filter(CabinCrew.vehicle_type_ids.any(vehicle_type_id))

    # Sort by attendant_id
    query = query.order_by(CabinCrew.attendant_id)

    # Execute the query with pagination
    paginated_crew = query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize the result
    crew_members = [{
      'attendant_id': crew.attendant_id,
      'name': crew.name,
      'age': crew.age,
      'gender': crew.gender,
      'nationality': crew.nationality,
      'known_languages': crew.known_languages,
      'attendant_type': crew.attendant_type,
      'vehicle_type_ids': crew.vehicle_type_ids,
      'dish_recipes': crew.dish_recipes,
      'scheduled_flights': crew.scheduled_flights,
      'aircraft_types': ['Boeing 737' if id == 1 else 'Airbus A320' if id == 2 else 'Boeing 777' for id in crew.vehicle_type_ids]
    } for crew in paginated_crew.items]

    response = {
        'crew_members': crew_members,
        'total': paginated_crew.total,
        'pages': paginated_crew.pages,
        'current_page': paginated_crew.page
    }

    return jsonify(response)


@cabin_crew.route('/create_cabin-crew', methods=['POST'])
@jwt_required()
def create_crew_member():
    data = request.get_json()

    # Required fields
    required_fields = ['name', 'age', 'gender', 'nationality', 'known_languages', 'attendant_type', 'vehicle_type_ids']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    name = data['name']
    age = data['age']
    gender = data['gender']
    nationality = data['nationality']
    known_languages = data['known_languages']
    attendant_type = data['attendant_type']
    vehicle_type_ids = data['vehicle_type_ids']

    # Validate that known_languages and vehicle_type_ids are lists
    if not isinstance(known_languages, list) or not all(isinstance(item, str) for item in known_languages):
        return jsonify({'error': 'known_languages must be an array of strings'}), 400
    
    # Ensure vehicle_type_ids is a list of integers and within allowed values
    allowed_vehicle_type_ids = {1, 2, 3}
    if not isinstance(vehicle_type_ids, list) or not all(isinstance(id, int) for id in vehicle_type_ids):
        return jsonify({'error': 'vehicle_type_ids must be an array of integers'}), 400
    if not all(id in allowed_vehicle_type_ids for id in vehicle_type_ids):
        return jsonify({'error': 'vehicle_type_ids must contain only 1, 2, or 3'}), 400

    # Additional properties based on attendant type
    dish_recipes = []
    if attendant_type == 'chef':
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
        dish_recipes = random.sample(dishes, random.randint(2, 4))

    # Create a new cabin crew member
    crew_member = CabinCrew(
        name=name,
        age=age,
        gender=gender,
        nationality=nationality,
        known_languages=known_languages,
        attendant_type=attendant_type,
        vehicle_type_ids=vehicle_type_ids,
        dish_recipes=dish_recipes if dish_recipes else None,
        scheduled_flights=[]
    )

    db.session.add(crew_member)
    db.session.commit()

    # Return crew member details
    return jsonify({
        'message': 'Crew member created successfully',
        'crew_member': {
            'attendant_id': crew_member.attendant_id,
            'name': crew_member.name,
            'age': crew_member.age,
            'gender': crew_member.gender,
            'nationality': crew_member.nationality,
            'known_languages': crew_member.known_languages,
            'attendant_type': crew_member.attendant_type,
            'vehicle_type_ids': crew_member.vehicle_type_ids,
            'dish_recipes': crew_member.dish_recipes,
            'scheduled_flights': crew_member.scheduled_flights
        }
    }), 201

