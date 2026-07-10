import copy
from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app


def test_signup_updates_activity_participants():
    # Arrange
    original_activities = copy.deepcopy(activities)
    client = TestClient(app)
    email = "student@mergington.edu"
    activity_name = "Chess Club"

    try:
        # Act
        signup_response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        activities_response = client.get("/activities")

        # Assert
        assert signup_response.status_code == 200
        assert activities_response.status_code == 200
        assert email in activities_response.json()[activity_name]["participants"]
    finally:
        activities.clear()
        activities.update(copy.deepcopy(original_activities))


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    original_activities = copy.deepcopy(activities)
    client = TestClient(app)
    email = "student@mergington.edu"
    activity_name = "Chess Club"

    try:
        # Act
        signup_response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        unregister_response = client.delete(
            f"/activities/{quote(activity_name)}/participants/{quote(email)}"
        )

        # Assert
        assert signup_response.status_code == 200
        assert unregister_response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities.clear()
        activities.update(copy.deepcopy(original_activities))
