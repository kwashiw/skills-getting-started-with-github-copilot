import copy
from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app


def test_signup_updates_activity_participants():
    original_activities = copy.deepcopy(activities)
    client = TestClient(app)

    try:
        email = "student@mergington.edu"
        activity_name = "Chess Club"

        signup_response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        assert signup_response.status_code == 200

        activities_response = client.get("/activities")
        assert activities_response.status_code == 200
        assert email in activities_response.json()[activity_name]["participants"]
    finally:
        activities.clear()
        activities.update(copy.deepcopy(original_activities))


def test_unregister_participant_removes_email_from_activity():
    original_activities = copy.deepcopy(activities)
    client = TestClient(app)

    try:
        email = "student@mergington.edu"
        activity_name = "Chess Club"

        signup_response = client.post(
            f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
        )
        assert signup_response.status_code == 200
        assert email in activities[activity_name]["participants"]

        unregister_response = client.delete(
            f"/activities/{quote(activity_name)}/participants/{quote(email)}"
        )

        assert unregister_response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities.clear()
        activities.update(copy.deepcopy(original_activities))
