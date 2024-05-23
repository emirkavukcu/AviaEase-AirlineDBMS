import unittest
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch
from backend.api.roster import create_roster_auto

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Example models to use in tests
class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(255), unique=True, nullable=False)
    aircraft_type_id = db.Column(db.String(255), nullable=False)

class FlightSeatAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.String(255), nullable=False)

class TestRosterAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def test_create_roster_auto_missing_fields(self):
        response = self.app.post('/create_roster_auto', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing fields', response.get_json()['error'])

    @patch('backend.api.roster.FlightSeatAssignment.query')
    def test_create_roster_auto_roster_already_exists(self, mock_query):
        mock_query.filter_by.return_value.first.return_value = True
        response = self.app.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('A roster for this flight already created', response.get_json()['message'])

    @patch('backend.api.roster.Flight.query')
    def test_create_roster_auto_invalid_flight_number(self, mock_query):
        mock_query.filter_by.return_value.first.return_value = None
        response = self.app.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid flight number', response.get_json()['error'])

    @patch('backend.api.roster.FlightSeatAssignment.query')
    @patch('backend.api.roster.Flight.query')
    @patch('backend.api.roster.seat_plan_auto')
    def test_create_roster_auto_success(self, mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query):
        mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
        mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
        mock_seat_plan_auto.return_value = "Roster successfully assigned"

        response = self.app.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Roster successfully assigned', response.get_json()['message'])

    @patch('backend.api.roster.FlightSeatAssignment.query')
    @patch('backend.api.roster.Flight.query')
    @patch('backend.api.roster.seat_plan_auto')
    def test_create_roster_auto_error_in_seat_plan_auto(self, mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query):
        mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
        mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
        mock_seat_plan_auto.return_value = "Error occurred"

        response = self.app.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
