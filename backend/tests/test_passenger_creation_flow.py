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
        "email": "passengertest@example.com",
        "password": "testpassword",
        "name": "Passenger Test User",
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

def test_fetch_passengers(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/passengers", headers=headers)
    assert response.status_code == 200

def test_create_passenger(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    passenger_data = {
        "name": "John Doe",
        "age": 35,
        "gender": "Male",
        "nationality": "American",
        "parent_id": None,
        "affiliated_passenger_ids": [],
        "scheduled_flights": []
    }
    response = requests.post(f"{BASE_URL}/create_passenger", headers=headers, json=passenger_data)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Passenger created successfully"
    assert "passenger" in data
    assert data["passenger"]["name"] == passenger_data["name"]

# If /create_passenger endpoint requires additional parameters, adjust the passenger_data accordingly.
