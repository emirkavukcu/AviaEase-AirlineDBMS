from flask import Blueprint, jsonify, request
from models import db, Passenger

passengers = Blueprint('passengers', __name__)

# Get passengers with optional filtering
@passengers.route('/passengers', methods=['GET'])
def get_passengers():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Filtering parameters
    passenger_id = request.args.get('passenger_id', type=int)
    name = request.args.get('name', type=str)
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    gender = request.args.get('gender', type=str)
    nationality = request.args.get('nationality', type=str)

    # Building the query
    query = Passenger.query

    if passenger_id:
        query = query.filter(Passenger.passenger_id == passenger_id)
    if name:
        query = query.filter(Passenger.name.ilike(f'%{name}%'))
    if min_age:
        query = query.filter(Passenger.age >= min_age)
    if max_age:
        query = query.filter(Passenger.age <= max_age)
    if gender:
        query = query.filter(Passenger.gender.ilike(gender))
    if nationality:
        query = query.filter(Passenger.nationality.ilike(f'%{nationality}%'))

    query = query.order_by(Passenger.passenger_id)

    # Sort by passenger_id
    query = query.order_by(Passenger.passenger_id)

    # Execute the query with pagination
    paginated_passengers = query.paginate(page=page, per_page=per_page, error_out=False)

    # Prepare detailed result
    passengers = [{
        'passenger_id': passenger.passenger_id,
        'name': passenger.name,
        'age': passenger.age,
        'gender': passenger.gender,
        'nationality': passenger.nationality,
        'parent_id': passenger.parent_id,
        'affiliated_passenger_ids': passenger.affiliated_passenger_ids,
        'scheduled_flights': passenger.scheduled_flights
    } for passenger in paginated_passengers.items]

    response = {
        'passengers': passengers,
        'total': paginated_passengers.total,
        'pages': paginated_passengers.pages,
        'current_page': paginated_passengers.page
    }
    return jsonify(response), 200

# Create a new passenger
@passengers.route('/create_passenger', methods=['POST'])
def create_passenger():
    data = request.get_json()  # Get data from JSON body

    # Check for required fields
    required_fields = ['name', 'age', 'gender', 'nationality']
    missing_fields = [field for field in required_fields if field not in data or data.get(field) is None]

    if missing_fields:
        return jsonify({'error': f'Missing required data: {", ".join(missing_fields)}'}), 400

    # Create new Passenger object
    new_passenger = Passenger(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        nationality=data['nationality'],
        parent_id=data.get('parent_id'),
        affiliated_passenger_ids=data.get('affiliated_passenger_ids', []),
        scheduled_flights=data.get('scheduled_flights', [])
    )

    # Add new passenger to the database session and commit it
    db.session.add(new_passenger)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

    # Return a success response
    return jsonify({'message': 'Passenger created successfully', 'passenger': {
        'passenger_id': new_passenger.passenger_id,
        'name': new_passenger.name,
        'age': new_passenger.age,
        'gender': new_passenger.gender,
        'nationality': new_passenger.nationality,
        'parent_id': new_passenger.parent_id,
        'affiliated_passenger_ids': new_passenger.affiliated_passenger_ids,
        'scheduled_flights': new_passenger.scheduled_flights
    }}), 201
