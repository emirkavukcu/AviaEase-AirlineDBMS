<<<<<<< HEAD
import pytest
from app import create_app, db
from models.airport import Airport
from config import TestConfig

@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.create_all()
        populate_db()
        yield db
        db.session.remove()
        db.drop_all()

def populate_db():
    airport1 = Airport(
        airport_code='AAA',
        name='Sample Airport 1',
        city='Sample City 1',
        country='AA',
        latitude=12.345678,
        longitude=98.765432
    )
    airport2 = Airport(
        airport_code='BBB',
        name='Sample Airport 2',
        city='Sample City 2',
        country='BB',
        latitude=23.456789,
        longitude=87.654321
    )
    db.session.add(airport1)
    db.session.add(airport2)
    db.session.commit()

def test_get_airport_codes(client, init_database):
    response = client.get('/api/airport_codes')
    data = response.get_json()
    assert response.status_code == 200
    assert 'AAA' in data
    assert 'BBB' in data

def test_get_airport_details(client, init_database):
    response = client.get('/api/airports')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert any(airport['airport_code'] == 'AAA' and airport['city'] == 'Sample City 1' and airport['country'] == 'AA' for airport in data)
    assert any(airport['airport_code'] == 'BBB' and airport['city'] == 'Sample City 2' and airport['country'] == 'BB' for airport in data)



=======
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch
from backend.app import create_app
from backend.models import db, Airport

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestAirportsAPI(unittest.TestCase):

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

    def test_get_airports_empty(self):
        response = self.client.get('/airport_codes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_airports_with_data(self):
        airport1 = Airport(airport_code='AAA', name='Airport A', city='City A', country='US', latitude=40.0, longitude=-74.0)
        airport2 = Airport(airport_code='BBB', name='Airport B', city='City B', country='US', latitude=41.0, longitude=-75.0)
        db.session.add_all([airport1, airport2])
        db.session.commit()

        response = self.client.get('/airport_codes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), ['AAA', 'BBB'])

    def test_get_airport_details_empty(self):
        response = self.client.get('/airports')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_airport_details_with_data(self):
        airport1 = Airport(airport_code='AAA', name='Airport A', city='City A', country='US', latitude=40.0, longitude=-74.0)
        airport2 = Airport(airport_code='BBB', name='Airport B', city='City B', country='GB', latitude=41.0, longitude=-75.0)
        db.session.add_all([airport1, airport2])
        db.session.commit()

        response = self.client.get('/airports')
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {"airport_code": "AAA", "city": "City A", "country": "United States"},
            {"airport_code": "BBB", "city": "City B", "country": "United Kingdom"}
        ]
        self.assertEqual(response.get_json(), expected_data)

    @patch('backend.api.airports.Airport.query')
    def test_get_airports_mock(self, mock_query):
        mock_query.all.return_value = [
            Airport(airport_code='AAA', name='Airport A', city='City A', country='US', latitude=40.0, longitude=-74.0),
            Airport(airport_code='BBB', name='Airport B', city='City B', country='GB', latitude=41.0, longitude=-75.0)
        ]
        response = self.client.get('/airport_codes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), ['AAA', 'BBB'])

    @patch('backend.api.airports.Airport.query')
    def test_get_airport_details_mock(self, mock_query):
        mock_query.all.return_value = [
            Airport(airport_code='AAA', name='Airport A', city='City A', country='US', latitude=40.0, longitude=-74.0),
            Airport(airport_code='BBB', name='Airport B', city='City B', country='GB', latitude=41.0, longitude=-75.0)
        ]
        response = self.client.get('/airports')
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {"airport_code": "AAA", "city": "City A", "country": "United States"},
            {"airport_code": "BBB", "city": "City B", "country": "United Kingdom"}
        ]
        self.assertEqual(response.get_json(), expected_data)

    def test_get_airport_details_invalid_country_code(self):
        airport1 = Airport(airport_code='AAA', name='Airport A', city='City A', country='XX', latitude=40.0, longitude=-74.0)
        db.session.add(airport1)
        db.session.commit()

        response = self.client.get('/airports')
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {"airport_code": "AAA", "city": "City A", "country": "XX"}
        ]
        self.assertEqual(response.get_json(), expected_data)

    def test_get_airport_details_country_not_found(self):
        airport1 = Airport(airport_code='AAA', name='Airport A', city='City A', country='ZZ', latitude=40.0, longitude=-74.0)
        db.session.add(airport1)
        db.session.commit()

        response = self.client.get('/airports')
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {"airport_code": "AAA", "city": "City A", "country": "ZZ"}
        ]
        self.assertEqual(response.get_json(), expected_data)

    @patch('backend.api.airports.pycountry.countries.get')
    def test_get_airport_details_pycountry_mock(self, mock_pycountry):
        mock_pycountry.return_value = None
        airport1 = Airport(airport_code='AAA', name='Airport A', city='City A', country='US', latitude=40.0, longitude=-74.0)
        db.session.add(airport1)
        db.session.commit()

        response = self.client.get('/airports')
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {"airport_code": "AAA", "city": "City A", "country": "US"}
        ]
        self.assertEqual(response.get_json(), expected_data)

if __name__ == '__main__':
    unittest.main()
>>>>>>> 2550ee0e0879812057734747f9de09014f341500
