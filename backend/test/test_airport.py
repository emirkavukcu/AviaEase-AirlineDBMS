import pytest
from backend.models.airport import Airport
from backend.models.base import db
from backend.app import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app()
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
        yield db
        db.session.remove()
        db.drop_all()

def test_airport_creation(init_database):
    airport = Airport(
        airport_code='ABC',
        name='Test Airport',
        city='Test City',
        country='Test Country',
        latitude=12.345678,
        longitude=98.765432
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.airport_code == 'ABC'

def test_airport_code(init_database):
    airport = Airport(
        airport_code='XYZ',
        name='Another Airport',
        city='Another City',
        country='Another Country',
        latitude=23.456789,
        longitude=87.654321
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.airport_code == 'XYZ'

def test_airport_name(init_database):
    airport = Airport(
        airport_code='DEF',
        name='Third Airport',
        city='Third City',
        country='Third Country',
        latitude=34.567890,
        longitude=76.543210
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.name == 'Third Airport'

def test_airport_city(init_database):
    airport = Airport(
        airport_code='GHI',
        name='Fourth Airport',
        city='Fourth City',
        country='Fourth Country',
        latitude=45.678901,
        longitude=65.432109
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.city == 'Fourth City'

def test_airport_country(init_database):
    airport = Airport(
        airport_code='JKL',
        name='Fifth Airport',
        city='Fifth City',
        country='Fifth Country',
        latitude=56.789012,
        longitude=54.321098
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.country == 'Fifth Country'

def test_airport_latitude(init_database):
    airport = Airport(
        airport_code='MNO',
        name='Sixth Airport',
        city='Sixth City',
        country='Sixth Country',
        latitude=67.890123,
        longitude=43.210987
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.latitude == 67.890123

def test_airport_longitude(init_database):
    airport = Airport(
        airport_code='PQR',
        name='Seventh Airport',
        city='Seventh City',
        country='Seventh Country',
        latitude=78.901234,
        longitude=32.109876
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.longitude == 32.109876

def test_airport_repr(init_database):
    airport = Airport(
        airport_code='STU',
        name='Eighth Airport',
        city='Eighth City',
        country='Eighth Country',
        latitude=89.012345,
        longitude=21.098765
    )
    db.session.add(airport)
    db.session.commit()
    assert repr(airport) == '<Airport STU - Eighth Airport>'

def test_duplicate_airport_code(init_database):
    airport1 = Airport(
        airport_code='VWX',
        name='Ninth Airport',
        city='Ninth City',
        country='Ninth Country',
        latitude=12.345678,
        longitude=98.765432
    )
    db.session.add(airport1)
    db.session.commit()

    airport2 = Airport(
        airport_code='VWX',
        name='Tenth Airport',
        city='Tenth City',
        country='Tenth Country',
        latitude=23.456789,
        longitude=87.654321
    )
    db.session.add(airport2)
    with pytest.raises(Exception):
        db.session.commit()

def test_airport_full_creation(init_database):
    airport = Airport(
        airport_code='YZX',
        name='Eleventh Airport',
        city='Eleventh City',
        country='Eleventh Country',
        latitude=12.345678,
        longitude=98.765432
    )
    db.session.add(airport)
    db.session.commit()
    assert airport.airport_code == 'YZX'
    assert airport.name == 'Eleventh Airport'
    assert airport.city == 'Eleventh City'
    assert airport.country == 'Eleventh Country'
    assert airport.latitude == 12.345678
    assert airport.longitude == 98.765432
