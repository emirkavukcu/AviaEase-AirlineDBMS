from flask import Blueprint, jsonify, request
from models import db, Pilot

pilots = Blueprint('pilots', __name__)

@pilots.route('/pilots', methods=['GET'])
def get_pilots():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Filter parameters
    pilot_id = request.args.get('pilot_id', type=int)
    name = request.args.get('name', type=str)
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    gender = request.args.get('gender', type=str)
    nationality = request.args.get('nationality', type=str)
    vehicle_type_id = request.args.get('vehicle_type_id', type=int)
    min_allowed_range = request.args.get('min_allowed_range', type=int)
    max_allowed_range = request.args.get('max_allowed_range', type=int)
    seniority_level = request.args.get('seniority_level', type=str)
    
    # Build query base
    query = Pilot.query
    
    # Applying filters
    if pilot_id:
        query = query.filter(Pilot.pilot_id == pilot_id)
    if name:
        query = query.filter(Pilot.name.ilike(f'%{name}%'))
    if min_age:
        query = query.filter(Pilot.age >= min_age)
    if max_age:
        query = query.filter(Pilot.age <= max_age)
    if gender:
        query = query.filter(Pilot.gender.ilike(gender))
    if nationality:
        query = query.filter(Pilot.nationality.ilike(f'%{nationality}%'))
    if vehicle_type_id:
        query = query.filter(Pilot.vehicle_type_id == vehicle_type_id)
    if min_allowed_range:
        query = query.filter(Pilot.allowed_range >= min_allowed_range)
    if max_allowed_range:
        query = query.filter(Pilot.allowed_range <= max_allowed_range)
    if seniority_level:
        query = query.filter(Pilot.seniority_level == seniority_level)
    

    # Sort by pilot_id
    query = query.order_by(Pilot.pilot_id)
    
    # Pagination
    paginated_pilots = query.paginate(page=page, per_page=per_page, error_out=False)
    pilots = [{
      'pilot_id': pilot.pilot_id,
      'name': pilot.name,
      'age': pilot.age,
      'gender': pilot.gender,
      'nationality': pilot.nationality,
      'vehicle_type_id': pilot.vehicle_type_id,
      'aircraft_type': 'Boeing 737' if pilot.vehicle_type_id == 1 else 'Airbus A320' if pilot.vehicle_type_id == 2 else 'Boeing 777',
      'allowed_range': pilot.allowed_range,
      'seniority_level': pilot.seniority_level,
      'known_languages': pilot.known_languages,
      'scheduled_flights': pilot.scheduled_flights
    } for pilot in paginated_pilots.items]
    
    return jsonify({
        'pilots': pilots,
        'total': paginated_pilots.total,
        'pages': paginated_pilots.pages,
        'current_page': page
    }), 200

@pilots.route('/create_pilot', methods=['POST'])
def create_pilot():
    data = request.get_json()

    # Required fields
    required_fields = ['name', 'age', 'gender', 'nationality', 'known_languages', 'vehicle_type_id', 'allowed_range', 'seniority_level']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    name = data['name']
    age = data['age']
    gender = data['gender']
    nationality = data['nationality']
    known_languages = data['known_languages']
    vehicle_type_id = data['vehicle_type_id']
    allowed_range = data['allowed_range']
    seniority_level = data['seniority_level']

    # Validate that known_languages is a list of strings
    if not isinstance(known_languages, list) or not all(isinstance(item, str) for item in known_languages):
        return jsonify({'error': 'known_languages must be an array of strings'}), 400
    
    # Validate vehicle_type_id is an integer and one of the allowed values
    allowed_vehicle_type_ids = {1, 2, 3}
    if not isinstance(vehicle_type_id, int) or vehicle_type_id not in allowed_vehicle_type_ids:
        return jsonify({'error': 'vehicle_type_id must be an integer and one of [1, 2, 3]'}), 400

    # Create a new pilot
    pilot = Pilot(
        name=name,
        age=age,
        gender=gender,
        nationality=nationality,
        known_languages=known_languages,
        vehicle_type_id=vehicle_type_id,
        allowed_range=allowed_range,
        seniority_level=seniority_level,
        scheduled_flights=[]
    )

    db.session.add(pilot)
    db.session.commit()

    # Return pilot details
    return jsonify({
        'message': 'Pilot created successfully',
        'pilot': {
            'pilot_id': pilot.pilot_id,
            'name': pilot.name,
            'age': pilot.age,
            'gender': pilot.gender,
            'nationality': pilot.nationality,
            'known_languages': pilot.known_languages,
            'vehicle_type_id': pilot.vehicle_type_id,
            'allowed_range': pilot.allowed_range,
            'seniority_level': pilot.seniority_level,
            'scheduled_flights': pilot.scheduled_flights
        }
    }), 201