from flask import Blueprint, request, jsonify
from models import db, Flight, Passenger, Pilot, CabinCrew
import random
from flask_jwt_extended import jwt_required

details = Blueprint('details', __name__)

@details.route('/details', methods=['GET'])
@jwt_required()
def get_details():
    print(request.headers)
    flights_count = Flight.query.count()
    passengers_count = Passenger.query.count()
    pilots_count = Pilot.query.count()
    cabincrew_count = CabinCrew.query.count()

    return jsonify({
        'flights': flights_count,
        'passengers': passengers_count,
        'pilots': pilots_count,
        'cabincrew': cabincrew_count
    }), 200