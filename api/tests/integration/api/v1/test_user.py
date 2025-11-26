import pytest
from fastapi.testclient import TestClient

from api.tests.integration.api import app
from api.tests.integration.db import clear_db


client = TestClient(app)

@pytest.fixture
def user():
    return {
        "name": "John",
        "phone": "+5519999999999",
        "address": "255 Lincoln Av.",
        "email": "john@doe.com"
    }


def test_get_all_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)


def test_create_user_successfully(user):
    response = client.post("/api/v1/users", json=user)
    created_user = response.json()
    assert response.status_code == 201

    assert created_user["name"] == user["name"]
    assert created_user["phone"] == "tel:+55-19-99999-9999"
    assert created_user["address"] == user["address"]
    assert created_user["email"] == user["email"]
    assert "created_at" in created_user
    assert "updated_at" in created_user


def _call_and_assert_endpoint_status(user, status):
    response = client.post("/api/v1/users", json=user)
    assert response.status_code == status


def test_create_user_missing_email(user):
    del user["email"]
    _call_and_assert_endpoint_status(user, 422)


def test_create_user_missing_name(user):
    del user["name"]
    _call_and_assert_endpoint_status(user, 422)


def test_create_user_missing_phone(user):
    del user["phone"]
    _call_and_assert_endpoint_status(user, 422)


def test_create_user_missing_address(user):
    del user["address"]
    _call_and_assert_endpoint_status(user, 422)


def test_create_user_invalid_email(user):
    user["email"] = "invalid"
    _call_and_assert_endpoint_status(user, 422)

def test_create_user_check_already_exists(user):
    _call_and_assert_endpoint_status(user, 201)

    response = client.post("/api/v1/users", json=user)
    assert response.status_code == 409
