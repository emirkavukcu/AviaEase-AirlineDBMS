import pytest
from app import create_app, db
from models import User
from config import TestConfig
import bcrypt
import os
import dotenv

dotenv.load_dotenv()

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
    # Populate with test user data
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    test_user = User(email='test@example.com', password=hashed_password, name='Test User')
    db.session.add(test_user)
    db.session.commit()

def test_register_success(client, init_database):
    response = client.post('/api/register', json={
        'email': 'newuser@example.com',
        'password': 'newpassword',
        'name': 'New User',
        'signCode': os.getenv('SIGN_CODE')
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'User registered'

def test_register_existing_user(client, init_database):
    response = client.post('/api/register', json={
        'email': 'test@example.com',
        'password': 'newpassword',
        'name': 'Test User',
        'signCode': os.getenv('SIGN_CODE')
    })
    data = response.get_json()
    assert response.status_code == 409
    assert data['message'] == 'User already exists'

def test_register_invalid_sign_code(client, init_database):
    response = client.post('/api/register', json={
        'email': 'anotheruser@example.com',
        'password': 'anotherpassword',
        'name': 'Another User',
        'signCode': 'invalidcode'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == 'Invalid sign code'

def test_login_success(client, init_database):
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data

def test_login_invalid_password(client, init_database):
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == 'Bad Email or Password'

def test_login_nonexistent_user(client, init_database):
    response = client.post('/api/login', json={
        'email': 'nonexistent@example.com',
        'password': 'password'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['message'] == 'Bad Email or Password'