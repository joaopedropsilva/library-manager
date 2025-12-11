import pytest

from fastapi.testclient import TestClient

from api.tests.api import app
from api.tests.config_defaults import settings


client = TestClient(app)


@pytest.mark.loan
def test_get_loans_paginated(create_loans):
    response = client.get("/api/v1/loans/")
    assert response.status_code == 200
    pagination_result = response.json()
    assert "total_items" in pagination_result
    assert "page_items" in pagination_result
    assert "page" in pagination_result
    assert "total_pages" in pagination_result
    assert pagination_result["total_items"] == 0

    skip=-1
    limit=5
    response = client.get(f"/api/v1/books/?skip={skip}&limit={limit}")
    assert response.status_code == 422
    skip=0
    limit=-1
    response = client.get(f"/api/v1/books/?skip={skip}&limit={limit}")
    assert response.status_code == 422

    insert_amount = 20
    create_loans(insert_amount)
    skip=0
    limit=5
    page_expected = skip // limit
    response = client.get(f"/api/v1/books/?skip={skip}&limit={limit}")
    pagination_result = response.json()
    assert pagination_result["total_items"] == insert_amount
    assert len(pagination_result["page_items"]) == limit
    assert pagination_result["page"] == page_expected


@pytest.mark.loan
def test_create_loan(loan_create, create_loans):
    invalid_uuid = "invalid"
    response = client.post(f"/api/v1/loans/?book_id={invalid_uuid}&user_id={invalid_uuid}")
    assert response.status_code == 422

    book_read, user_read = loan_create

    fake_book_id = "292ada19-6b06-44f7-a20e-dc6687668b0e"
    response = client.post(f"/api/v1/loans/?book_id={fake_book_id}&user_id={str(user_read.id)}")
    assert response.status_code == 404

    fake_user_id = "292ada19-6b06-44f7-a20e-dc6687668b0e"
    response = client.post(f"/api/v1/loans/?book_id={str(book_read.id)}&user_id={fake_user_id}")
    assert response.status_code == 404

    response = client.post(f"/api/v1/loans/?book_id={str(book_read.id)}&user_id={str(user_read.id)}")
    assert response.status_code == 201

    response = client.get(f"/api/v1/books/{book_read.isbn}")
    assert response.status_code == 200
    fetched_book = response.json()
    assert fetched_book["is_available"] == False

    created_loans = create_loans(settings.max_active_loans_per_user, user_read)
    new_book_id = created_loans[0].book_id
    response = client.post(f"/api/v1/loans/?book_id={str(new_book_id)}&user_id={str(user_read.id)}")
    assert response.status_code == 422
