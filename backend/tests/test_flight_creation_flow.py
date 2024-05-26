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
        "email": "flighttest@example.com",
        "password": "testpassword",
        "name": "Flight Test User",
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

def test_fetch_flights(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/flights", headers=headers)
    assert response.status_code == 200

def test_create_flight(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    flight_data = {
        "flight_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "source": "JFK",
        "destination": "LAX",
        "vehicle_type_id": 1,
        "create_roster": "Yes"
        }
    response = requests.post(f"{BASE_URL}/create_flight", headers=headers, json=flight_data)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Flight created and roster successfully assigned"