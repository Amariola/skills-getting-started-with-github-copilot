def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert isinstance(data[expected_activity]["participants"], list)
    assert "max_participants" in data[expected_activity]
    assert len(data) >= 1


def test_get_activities_includes_activity_details(client):
    # Arrange
    activity_name = "Programming Class"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    activity = data[activity_name]
    assert activity["description"]
    assert activity["schedule"]
    assert activity["max_participants"] == 20
