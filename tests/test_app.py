from src.app import activities


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"].startswith("Learn strategies")
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_new_participant(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_participant(client):
    email = "duplicate-test@mergington.edu"
    first_response = client.post("/activities/Programming%20Class/signup", params={"email": email})
    assert first_response.status_code == 200

    second_response = client.post("/activities/Programming%20Class/signup", params={"email": email})
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"


def test_remove_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name.replace(' ', '%20')}/participants/{email.replace('@', '%40')}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_remove_nonexistent_participant(client):
    response = client.delete("/activities/Chess%20Club/participants/nonexistent%40mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_from_missing_activity(client):
    response = client.delete("/activities/Nonexistent%20Club/participants/test%40example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
