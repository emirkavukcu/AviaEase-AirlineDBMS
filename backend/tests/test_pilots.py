import pytest
from app import create_app, db
from models import Pilot
from config import TestConfig
import json

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
    pilot1 = Pilot(
        name='Tom Hanks',
        age=45,
        gender='Male',
        nationality='American',
        vehicle_type_ids=[1, 2],
        scheduled_flights=[]
    )
    pilot2 = Pilot(
        name='Emily Blunt',
        age=35,
        gender='Female',
        nationality='British',
        vehicle_type_ids=[2, 3],
        scheduled_flights=[]
    )
    pilot3 = Pilot(
        name='John Smith',
        age=40,
        gender='Male',
        nationality='Canadian',
        vehicle_type_ids=[1, 3],
        scheduled_flights=[]
    )
    db.session.add(pilot1)
    db.session.add(pilot2)
    db.session.add(pilot3)
    db.session.commit()

def test_get_pilots(client, init_database):
    response = client.get('/pilots')
    data = response.get_json()
    print("Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data['pilots']) == 3
    assert any(pilot['name'] == 'Tom Hanks' and pilot['nationality'] == 'American' for pilot in data['pilots'])
    assert any(pilot['name'] == 'Emily Blunt' and pilot['nationality'] == 'British' for pilot in data['pilots'])
    assert any(pilot['name'] == 'John Smith' and pilot['nationality'] == 'Canadian' for pilot in data['pilots'])

def test_create_pilot(client, init_database):
    new_pilot_data = {
        'name': 'Michael Jordan',
        'age': 50,
        'gender': 'Male',
        'nationality': 'American',
        'vehicle_type_ids': [1, 2]
    }
    response = client.post('/create_pilot', data=json.dumps(new_pilot_data), content_type='application/json')
    data = response.get_json()
    print("Response Data:", data)  # Debugging print
    assert response.status_code == 201
    assert data['message'] == 'Pilot created successfully'
    assert data['pilot']['name'] == 'Michael Jordan'
    assert data['pilot']['nationality'] == 'American'

def test_get_pilots_with_filters(client, init_database):
    response = client.get('/pilots?name=Tom Hanks')
    data = response.get_json()
    print("Filtered Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['name'] == 'Tom Hanks'

def test_get_pilots_with_multiple_filters(client, init_database):
    response = client.get('/pilots?min_age=30&max_age=40&gender=Female&nationality=British')
    data = response.get_json()
    print("Multiple Filters Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data['pilots']) == 1
    assert data['pilots'][0]['name'] == 'Emily Blunt'
    assert data['pilots'][0]['age'] == 35
    assert data['pilots'][0]['gender'] == 'Female'
    assert data['pilots'][0]['nationality'] == 'British'

def test_get_pilots_with_all_filters(client, init_database):
    response = client.get('/pilots?pilot_id=3&name=John Smith&min_age=35&max_age=45&gender=Male&nationality=Canadian&licenses=Private&vehicle_type_ids=1&vehicle_type_ids=3')
    data = response.get_json()
    print("All Filters Response Data:", data
