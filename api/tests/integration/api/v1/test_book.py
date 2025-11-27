import pytest
from fastapi.testclient import TestClient

from api.tests.integration.api import app


client = TestClient(app)


@pytest.mark.book
def test_get_book_by_isbn(book, create_book):
    response = client.get("/api/v1/books/invalid")
    assert response.status_code == 422

    create_book()
    response = client.get(f"/api/v1/books/{book.isbn}")
    assert response.status_code == 200


@pytest.mark.book
def test_create_book(book):
    response = client.post("/api/v1/books", json=book.model_dump())
    created_book = response.json()
    assert response.status_code == 201
    assert "id" in created_book
    assert created_book["title"] == book.title
    assert created_book["publisher"] == book.publisher
    assert created_book["isbn"] == book.isbn
    assert created_book["category"] == book.category
    assert created_book["synopsis"] == book.synopsis
    assert "author_names" in created_book
    assert "is_available" in created_book
    assert "created_at" in created_book
    assert "updated_at" in created_book

    book_create_schema = book.model_dump()
    book_copy = copy.deepcopy(book_create_schema)
    del book_copy["title"]
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422

    book_copy = copy.deepcopy(book_create_schema)
    del book_copy["isbn"]
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422

    book_copy = copy.deepcopy(book_create_schema)
    book_copy["author_ids"] = []
    response = client.post("/api/v1/books", json=book_copy)
    assert response.status_code == 422

    book_copy = copy.deepcopy(book_create_schema)
    book_copy["isbn"] = "invalid"
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
