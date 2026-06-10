import os
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

import app as app_module


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"
    params = {"email": email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    params = {"email": "student@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_already_registered_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    params = {"email": email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=params)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Already registered for this activity"


def test_signup_for_activity_at_capacity_returns_400(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "overflow@mergington.edu"
    activity = app_module.activities[activity_name]
    activity["participants"] = [f"user{i}@mergington.edu" for i in range(activity["max_participants"])]
    params = {"email": email}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=params)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is at maximum capacity"
