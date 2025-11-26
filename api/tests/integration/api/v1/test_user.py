import uuid

import pytest
from fastapi.testclient import TestClient

from api.tests.integration.api import app


client = TestClient(app)


def test_get_user_by_id(create_valid_user):
    response = client.get("/api/v1/users/invalid")
    assert response.status_code == 404

    response = client.get(f"/api/v1/users/{uuid.uuid4()}")
    assert response.status_code == 404

    created_user = create_valid_user()
    response = client.get(f"/api/v1/users/{created_user.id}")
    user = response.json()
    assert response.status_code == 200
    assert user["id"] == str(created_user.id)
    assert user["name"] == created_user.name
    assert user["phone"] == created_user.phone
    assert user["address"] == created_user.address
    assert user["email"] == created_user.email
    assert "created_at" in user
    assert "updated_at" in user


def test_get_all_users_paginated(seed_db_with_users):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    pagination_result = response.json()
    assert "total_items" in pagination_result
    assert "page_items" in pagination_result
    assert "page" in pagination_result
    assert "total_pages" in pagination_result
    assert pagination_result["total_items"] == 0

    skip=-1
    limit=5
    response = client.get(f"/api/v1/users/?skip={skip}&limit={limit}")
    assert response.status_code == 422
    skip=0
    limit=-1
    response = client.get(f"/api/v1/users/?skip={skip}&limit={limit}")
    assert response.status_code == 422

    insert_amount = 20
    seed_db_with_users(insert_amount)
    skip=0
    limit=5
    page_expected = skip // limit + 1
    response = client.get(f"/api/v1/users/?skip={skip}&limit={limit}")
    pagination_result = response.json()
    assert pagination_result["total_items"] == insert_amount
    assert len(pagination_result["page_items"]) == limit
    assert pagination_result["page"] == page_expected


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
