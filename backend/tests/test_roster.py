import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch
from backend.app import create_app
from backend.models import db, Flight, FlightSeatAssignment

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestRosterAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_class=TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def test_create_roster_auto_missing_fields(self):
        response = self.client.post('/create_roster_auto', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing fields', response.get_json()['error'])

    @patch('backend.api.roster.FlightSeatAssignment.query')
    def test_create_roster_auto_roster_already_exists(self, mock_query):
        mock_query.filter_by.return_value.first.return_value = True
        response = self.client.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('A roster for this flight already created', response.get_json()['message'])

    @patch('backend.api.roster.Flight.query')
    def test_create_roster_auto_invalid_flight_number(self, mock_query):
        mock_query.filter_by.return_value.first.return_value = None
        response = self.client.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid flight number', response.get_json()['error'])

    @patch('backend.api.roster.FlightSeatAssignment.query')
    @patch('backend.api.roster.Flight.query')
    @patch('backend.api.roster.seat_plan_auto')
    def test_create_roster_auto_success(self, mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query):
        mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
        mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
        mock_seat_plan_auto.return_value = "Roster successfully assigned"

        response = self.client.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Roster successfully assigned', response.get_json()['message'])

    @patch('backend.api.roster.FlightSeatAssignment.query')
    @patch('backend.api.roster.Flight.query')
    @patch('backend.api.roster.seat_plan_auto')
    def test_create_roster_auto_error_in_seat_plan_auto(self, mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query):
        mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
        mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
        mock_seat_plan_auto.return_value = "Error occurred"

        response = self.client.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error occurred', response.get_json()['message'])

    def test_create_roster_auto_no_json(self):
        response = self.client.post('/create_roster_auto', data='Not a JSON')
        self.assertEqual(response.status_code, 400)

    def test_create_roster_auto_empty_flight_number(self):
        response = self.client.post('/create_roster_auto', json={'flight_number': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid flight number', response.get_json()['error'])

    def test_create_roster_auto_non_existent_flight(self):
        response = self.client.post('/create_roster_auto', json={'flight_number': 'NONEXISTENT'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid flight number', response.get_json()['error'])

    def test_create_roster_auto_invalid_json_structure(self):
        response = self.client.post('/create_roster_auto', json={'invalid_field': 'value'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing fields', response.get_json()['error'])

    @patch('backend.api.roster.FlightSeatAssignment.query')
    @patch('backend.api.roster.Flight.query')
    @patch('backend.api.roster.seat_plan_auto')
    def test_create_roster_auto_seat_plan_auto_exception(self, mock_seat_plan_auto, mock_flight_query, mock_flight_seat_assignment_query):
        mock_flight_seat_assignment_query.filter_by.return_value.first.return_value = None
        mock_flight_query.filter_by.return_value.first.return_value = Flight(flight_number='AB123', aircraft_type_id='Type1')
        mock_seat_plan_auto.side_effect = Exception("Unexpected error")

        response = self.client.post('/create_roster_auto', json={'flight_number': 'AB123'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('Unexpected error', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
