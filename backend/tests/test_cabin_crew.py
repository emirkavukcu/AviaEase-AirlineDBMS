import pytest
from app import create_app, db
from models import CabinCrew
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
    crew_member1 = CabinCrew(
        name='John Doe',
        age=30,
        gender='Male',
        nationality='American',
        known_languages=['English', 'Spanish'],
        attendant_type='chief',
        vehicle_type_ids=[1, 2],
        dish_recipes=[],
        scheduled_flights=[]
    )
    crew_member2 = CabinCrew(
        name='Jane Smith',
        age=25,
        gender='Female',
        nationality='Canadian',
        known_languages=['English', 'French'],
        attendant_type='regular',
        vehicle_type_ids=[2, 3],
        dish_recipes=[],
        scheduled_flights=[]
    )
    crew_member3 = CabinCrew(
        name='Alice Johnson',
        age=35,
        gender='Female',
        nationality='British',
        known_languages=['English'],
        attendant_type='chef',
        vehicle_type_ids=[1, 3],
        dish_recipes=['Grilled Salmon with Dill Sauce', 'Vegetable Lasagna'],
        scheduled_flights=[]
    )
    db.session.add(crew_member1)
    db.session.add(crew_member2)
    db.session.add(crew_member3)
    db.session.commit()

def test_get_crew_members(client, init_database):
    response = client.get('/cabin-crew')
    data = response.get_json()
    print("Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data['crew_members']) == 3
    assert any(member['name'] == 'John Doe' and member['nationality'] == 'American' for member in data['crew_members'])
    assert any(member['name'] == 'Jane Smith' and member['nationality'] == 'Canadian' for member in data['crew_members'])
    assert any(member['name'] == 'Alice Johnson' and member['nationality'] == 'British' for member in data['crew_members'])

def test_create_crew_member(client, init_database):
    new_member_data = {
        'name': 'Bob Brown',
        'age': 28,
        'gender': 'Male',
        'nationality': 'Australian',
        'known_languages': ['English'],
        'attendant_type': 'chef',
        'vehicle_type_ids': [1, 3]
    }
    response = client.post('/create_cabin-crew', data=json.dumps(new_member_data), content_type='application/json')
    data = response.get_json()
    print("Response Data:", data)  # Debugging print
    assert response.status_code == 201
    assert data['message'] == 'Crew member created successfully'
    assert data['crew_member']['name'] == 'Bob Brown'
    assert data['crew_member']['nationality'] == 'Australian'

def test_get_crew_members_with_filters(client, init_database):
    response = client.get('/cabin-crew?name=John Doe')
    data = response.get_json()
    print("Filtered Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data['crew_members']) == 1
    assert data['crew_members'][0]['name'] == 'John Doe'

def test_get_crew_members_with_multiple_filters(client, init_database):
    response = client.get('/cabin-crew?min_age=25&max_age=30&gender=Female&nationality=Canadian')
    data = response.get_json()
    print("Multiple Filters Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data['crew_members']) == 1
    assert data['crew_members'][0]['name'] == 'Jane Smith'
    assert data['crew_members'][0]['age'] == 25
    assert data['crew_members'][0]['gender'] == 'Female'
    assert data['crew_members'][0]['nationality'] == 'Canadian'

def test_get_crew_members_with_all_filters(client, init_database):
    response = client.get('/cabin-crew?attendant_id=3&name=Alice Johnson&min_age=30&max_age=40&gender=Female&nationality=British&attendant_type=chef&vehicle_type_ids=1&vehicle_type_ids=3')
    data = response.get_json()
    print("All Filters Response Data:", data)  # Debugging print
    assert response.status_code == 200
    assert len(data['crew_members']) == 1
    assert data['crew_members'][0]['name'] == 'Alice Johnson'
    assert data['crew_members'][0]['age'] == 35
    assert data['crew_members'][0]['gender'] == 'Female'
    assert data['crew_members'][0]['nationality'] == 'British'
    assert data['crew_members'][0]['attendant_type'] == 'chef'
    assert data['crew_members'][0]['vehicle_type_ids'] == [1, 3]
    assert 'Grilled Salmon with Dill Sauce' in data['crew_members'][0]['dish_recipes']

