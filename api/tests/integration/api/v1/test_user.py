import uuid
import copy

import pytest
from fastapi.testclient import TestClient

from api.tests.integration.api import app


client = TestClient(app)


@pytest.mark.user
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


@pytest.mark.user
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
    page_expected = skip // limit
    response = client.get(f"/api/v1/users/?skip={skip}&limit={limit}")
    pagination_result = response.json()
    assert pagination_result["total_items"] == insert_amount
    assert len(pagination_result["page_items"]) == limit
    assert pagination_result["page"] == page_expected


@pytest.mark.user
def test_create_user(user):
    response = client.post("/api/v1/users", json=user.model_dump())
    created_user = response.json()
    assert response.status_code == 201
    assert "id" in created_user
    assert created_user["name"] == user.name
    assert created_user["phone"] == user.phone
    assert created_user["address"] == user.address
    assert created_user["email"] == user.email
    assert "created_at" in created_user
    assert "updated_at" in created_user

    user_create_schema = user.model_dump()
    user_copy = copy.deepcopy(user_create_schema)
    del user_copy["name"]
    response = client.post("/api/v1/users", json=user_copy)
    assert response.status_code == 422

    user_copy = copy.deepcopy(user_create_schema)
    del user_copy["phone"]
    response = client.post("/api/v1/users", json=user_copy)
    assert response.status_code == 422

    user_copy = copy.deepcopy(user_create_schema)
    del user_copy["address"]
    response = client.post("/api/v1/users", json=user_copy)
    assert response.status_code == 422

    user_copy = copy.deepcopy(user_create_schema)
    del user_copy["email"]
    response = client.post("/api/v1/users", json=user_copy)
    assert response.status_code == 422

    user_copy = copy.deepcopy(user_create_schema)
    user_copy["email"] = "invalid"
    response = client.post("/api/v1/users", json=user_copy)
    assert response.status_code == 422


@pytest.mark.user
def test_create_user_already_exists(create_valid_user):
    user_read = create_valid_user()
    user_create = user_read.model_dump()
    del user_create["id"]
    del user_create["created_at"]
    del user_create["updated_at"]
    response = client.post("/api/v1/users", json=user_create)
    assert response.status_code == 409
