from locust import HttpUser, TaskSet, task, between
import os
import dotenv
from datetime import datetime, timedelta

dotenv.load_dotenv()

SIGN_CODE = os.getenv('SIGN_CODE')

class UserBehavior(TaskSet):
    token = None

    def on_start(self):
        """ called when a Locust start before any task is scheduled """
        if not UserBehavior.token:
            self.register_and_login()

    def register_and_login(self):
        # Register user (only if not already registered)
        register_response = self.client.post("/api/register", json={
            "email": "testuser@example.com",
            "password": "testpassword",
            "name": "Test User",
            "signCode": SIGN_CODE
        })
        if register_response.status_code not in [200, 201, 409]:  # 409 if already exists
            print("Failed to register user")

        # Login user
        login_response = self.client.post("/api/login", json={
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        if login_response.status_code == 200:
            UserBehavior.token = login_response.json()["access_token"]
        else:
            print("Failed to login user")

    @task(1)
    def get_flights(self):
        if UserBehavior.token:
            self.client.get("/api/flights", headers={"Authorization": f"Bearer {UserBehavior.token}"})

    @task(1)
    def get_flights_with_filters(self):
        if UserBehavior.token:
            now = datetime.now().isoformat()

            self.client.get("/api/flights?flight_number=100", headers={"Authorization": f"Bearer {UserBehavior.token}"})
            self.client.get("/api/flights?max_duration=180", headers={"Authorization": f"Bearer {UserBehavior.token}"})
            self.client.get("/api/flights?max_distance=1000", headers={"Authorization": f"Bearer {UserBehavior.token}"})
            self.client.get("/api/flights?source_airport=JFK", headers={"Authorization": f"Bearer {UserBehavior.token}"})
            self.client.get("/api/flights?source_city=New York", headers={"Authorization": f"Bearer {UserBehavior.token}"})
            self.client.get("/api/flights?source_country=USA", headers={"Authorization": f"Bearer {UserBehavior.token}"})
            self.client.get("/api/flights?aircraft_type_id=1", headers={"Authorization": f"Bearer {UserBehavior.token}"})
            self.client.get("/api/flights?status=pending", headers={"Authorization": f"Bearer {UserBehavior.token}"})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)

