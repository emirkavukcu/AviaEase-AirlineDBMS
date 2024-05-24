from flask import Blueprint, jsonify, request
from models import db, Airport, Flight, AircraftType
from services import calculate_distance, seat_plan_auto
from datetime import datetime, timedelta
from sqlalchemy import cast, String 
import pycountry

airports = Blueprint('airports', __name__)

@airports.route('/airport_codes', methods=['GET'])
def get_airports():
  airports = Airport.query.all()
  airports_data = [  
    airport.airport_code    
    for airport in airports
  ]
  return jsonify(airports_data), 200

from flask import jsonify
import pycountry

@airports.route('/airports', methods=['GET'])
def get_airport_details():
    airports = Airport.query.all()
    
    def get_country_name(country_code):
        try:
            country = pycountry.countries.get(alpha_2=country_code)
            return country.name
        except AttributeError:
            return country_code  # Return the code if the name is not found

    airports_data = [
        {
            "airport_code": airport.airport_code,
            "city": airport.city,
            "country": get_country_name(airport.country),
        }
        for airport in airports
    ]
    return jsonify(airports_data), 200

