import copy
import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    """Make a deep copy of the in-memory activities and restore after each test."""
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(orig)


def test_get_activities_contains_known_activity():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_adds_participant_and_reflected_in_get():
    email = "pytest_user@example.com"
    activity_name = "Chess Club"
    url_activity = urllib.parse.quote(activity_name, safe="")

    resp = client.post(f"/activities/{url_activity}/signup?email={urllib.parse.quote(email, safe='')}")
    assert resp.status_code == 200

    # verify participant appears in the activities payload
    activities_payload = client.get("/activities").json()
    assert email in activities_payload[activity_name]["participants"]


def test_signup_duplicate_returns_400():
    email = "dup_user@example.com"
    activity_name = "Chess Club"
    url_activity = urllib.parse.quote(activity_name, safe="")

    r1 = client.post(f"/activities/{url_activity}/signup?email={urllib.parse.quote(email, safe='')}")
    assert r1.status_code == 200

    # second signup should fail with 400
    r2 = client.post(f"/activities/{url_activity}/signup?email={urllib.parse.quote(email, safe='')}")
    assert r2.status_code == 400


def test_unregister_removes_participant():
    email = "to_remove@example.com"
    activity_name = "Chess Club"
    url_activity = urllib.parse.quote(activity_name, safe="")

    # signup first
    r1 = client.post(f"/activities/{url_activity}/signup?email={urllib.parse.quote(email, safe='')}")
    assert r1.status_code == 200

    # now unregister
    r2 = client.delete(f"/activities/{url_activity}/unregister?email={urllib.parse.quote(email, safe='')}")
    assert r2.status_code == 200

    data = client.get("/activities").json()
    assert email not in data[activity_name]["participants"]


def test_unregister_nonexistent_returns_404():
    email = "not_in_activity@example.com"
    activity_name = "Chess Club"
    url_activity = urllib.parse.quote(activity_name, safe="")

    r = client.delete(f"/activities/{url_activity}/unregister?email={urllib.parse.quote(email, safe='')}")
    assert r.status_code == 404
from fastapi.testclient import TestClient
import copy
import 
pip3 install pytest


from src.app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    # make a deep copy of the in-memory activities and restore after each test
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(orig)


def test_get_activities_contains_known_activity():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_adds_participant_and_reflected_in_get():
    email = "pytest_user@example.com"
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert resp.status_code == 200
    # verify participant appears in the activities payload
    activities_payload = client.get("/activities").json()
    assert email in activities_payload["Chess Club"]["participants"]


def test_unregister_removes_participant():
    email = "to_remove@example.com"
    # signup first
    r1 = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert r1.status_code == 200

    # now unregister
    r2 = client.delete(f"/activities/Chess%20Club/unregister?email={email}")
    assert r2.status_code == 200

    data = client.get("/activities").json()
    assert email not in data["Chess Club"]["participants"]
