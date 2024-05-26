import pytest
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000/api')
SIGN_CODE = os.getenv('SIGN_CODE')

@pytest.fixture(scope='module')
def user_data():
    return {
        "email": "pilottest@example.com",
        "password": "testpassword",
        "name": "Pilot Test User",
        "signCode": SIGN_CODE
    }

@pytest.fixture(scope='module')
def register_user(user_data):
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    return response

def test_register_user(register_user):
    assert register_user.status_code in [200, 201, 409]  # 409 if user already exists

@pytest.fixture(scope='module')
def login_user(user_data):
    response = requests.post(f"{BASE_URL}/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    return response

def test_login_user(login_user):
    assert login_user.status_code == 200
    data = login_user.json()
    assert "access_token" in data

@pytest.fixture(scope='module')
def access_token(login_user):
    data = login_user.json()
    return data["access_token"]

def test_fetch_pilots(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/pilots", headers=headers)
    assert response.status_code == 200

def test_create_pilot(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    pilot_data = {
        "name": "Captain John",
        "age": 45,
        "gender": "Male",
        "nationality": "American",
        "known_languages": ["English", "Spanish"],
        "vehicle_type_id": 1,
        "allowed_range": 8000,
        "seniority_level": "senior"
    }
    response = requests.post(f"{BASE_URL}/create_pilot", headers=headers, json=pilot_data)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Pilot created successfully"
    assert "pilot" in data
    assert data["pilot"]["name"] == pilot_data["name"]

# If /create_pilot endpoint requires additional parameters, adjust the pilot_data accordingly.
