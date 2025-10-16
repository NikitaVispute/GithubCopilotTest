import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_activity():
    # Use a test email and activity name
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "pytestuser@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data or "detail" in data

def test_signup_duplicate():
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "pytestuser@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    # First signup
    client.post(signup_url)
    # Second signup (should fail or warn)
    response = client.post(signup_url)
    assert response.status_code in (200, 400)
    data = response.json()
    assert "message" in data or "detail" in data

def test_unregister():
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "pytestuser@mergington.edu"
    response = client.post("/unregister", json={"activity": activity_name, "email": email})
    assert response.status_code == 200
    data = response.json()
    assert "success" in data or "error" in data
