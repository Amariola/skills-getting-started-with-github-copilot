def test_unregister_from_activity_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    params = {"email": email}

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_from_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    params = {"email": "student@mergington.edu"}

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_for_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Programming Class"
    params = {"email": "unknown@mergington.edu"}

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
