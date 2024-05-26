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
        airport_code='ZZZ',
        name='Sample Airport 2',
        city='Sample City 2',
        country='ZZ',
        latitude=23.456789,
        longitude=87.654321
    )
    db.session.add(airport1)
    db.session.add(airport2)
    db.session.commit()

def test_get_airport_codes(client, init_database):
    response = client.get('/airport_codes')
    data = response.get_json()
    assert response.status_code == 200
    assert 'AAA' in data
    assert 'ZZZ' in data

def test_get_airport_details(client, init_database):
    response = client.get('/airports')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert any(airport['airport_code'] == 'AAA' and airport['city'] == 'Sample City 1' and airport['country'] == 'AA' for airport in data)
    assert any(airport['airport_code'] == 'ZZZ' and airport['city'] == 'Sample City 2' and airport['country'] == 'ZZ' for airport in data)

def test_get_airport_codes_empty_db(client):
    response = client.get('/airport_codes')
    data = response.get_json()
    assert response.status_code == 200
    assert data == []

def test_get_airport_details_empty_db(client):
    response = client.get('/airports')
    data = response.get_json()
    assert response.status_code == 200
    assert data == []

def test_get_airport_details_country_code(client, init_database):
    response = client.get('/airports')
    data = response.get_json()
    assert response.status_code == 200
    assert any(airport['country'] == 'AA' for airport in data)

def test_get_airport_details_country_name(client, init_database):
    response = client.get('/airports')
    data = response.get_json()
    assert response.status_code == 200
    assert any(airport['country'] == 'AA' for airport in data)

def test_get_airport_codes_specific_airport(client, init_database):
    response = client.get('/airport_codes')
    data = response.get_json()
    assert response.status_code == 200
    assert 'AAA' in data

def test_get_airport_details_specific_airport(client, init_database):
    response = client.get('/airports')
    data = response.get_json()
    assert response.status_code == 200
    assert any(airport['airport_code'] == 'AAA' for airport in data)

def test_get_airport_codes_multiple_airports(client, init_database):
    response = client.get('/airport_codes')
    data = response.get_json()
    assert response.status_code == 200
    assert 'AAA' in data
    assert 'ZZZ' in data

def test_get_airport_details_multiple_airports(client, init_database):
    response = client.get('/airports')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert any(airport['airport_code'] == 'AAA' for airport in data)
    assert any(airport['airport_code'] == 'ZZZ' for airport in data)
