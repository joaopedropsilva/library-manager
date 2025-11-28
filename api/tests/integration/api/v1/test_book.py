import copy

import pytest
from fastapi.testclient import TestClient

from api.tests.integration.api import app


client = TestClient(app)


@pytest.mark.book
def test_get_book_by_isbn(create_book):
    response = client.get("/api/v1/books/invalid")
    assert response.status_code == 422

    isbn = create_book().isbn
    response = client.get(f"/api/v1/books/{isbn}")
    book_read = response.json()
    assert response.status_code == 200
    assert book_read["is_available"]


@pytest.mark.book
def test_get_books_paginated(create_books):
    response = client.get("/api/v1/books/")
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
    create_books(insert_amount)
    skip=0
    limit=5
    page_expected = skip // limit
    response = client.get(f"/api/v1/books/?skip={skip}&limit={limit}")
    pagination_result = response.json()
    assert pagination_result["total_items"] == insert_amount
    assert len(pagination_result["page_items"]) == limit
    assert pagination_result["page"] == page_expected


@pytest.mark.book
def test_create_book(book_create):
    response = client.post("/api/v1/books", json=book_create.model_dump())
    book_read_dict = response.json()
    assert response.status_code == 201
    assert "id" in book_read_dict
    assert book_read_dict["title"] == book_create.title
    assert book_read_dict["publisher"] == book_create.publisher
    assert book_read_dict["isbn"] == book_create.isbn
    assert book_read_dict["category"] == book_create.category
    assert book_read_dict["synopsis"] == book_create.synopsis
    assert book_read_dict["is_available"]
    assert "authors" in book_read_dict
    assert "created_at" in book_read_dict
    assert "updated_at" in book_read_dict

    book_create_schema = book_create.model_dump()
    book_copy = copy.deepcopy(book_create_schema)
    del book_copy["title"]
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422

    book_copy = copy.deepcopy(book_create_schema)
    del book_copy["publisher"]
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422

    book_copy = copy.deepcopy(book_create_schema)
    del book_copy["isbn"]
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422

    book_copy = copy.deepcopy(book_create_schema)
    book_copy["isbn"] = "invalid_isbn"
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422

    book_copy = copy.deepcopy(book_create_schema)
    del book_copy["authors"]
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422


@pytest.mark.book
def test_create_book_already_exists(create_book):
    book_read = create_book()
    book_create = book_read.model_dump()
    del book_create["id"]
    del book_create["created_at"]
    del book_create["updated_at"]
    del book_create["is_available"]
    response = client.post("/api/v1/books", json=book_create)
    assert response.status_code == 409
