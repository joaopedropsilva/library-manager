import random
from typing import Callable

import pytest

from api.versions.v1.schema.book import BookCreate, BookRead
from api.versions.v1.schema.author import AuthorCreate
from api.tests.db import Book, Author


@pytest.fixture
def author_create() -> AuthorCreate:
    author_dict = {
        "name": "Fernando Sabino",
        "description": "Autor mineiro"
    }

    return AuthorCreate(**author_dict)


@pytest.fixture
def callable_book_create(author_create):
    def _to_model(custom_book: dict = None) -> BookCreate:
        default_book_dict = {
            "title": "O Encontro Marcado",
            "publisher": "Record",
            "isbn": "9788501912008",
            "category": "literature",
            "synopsis": "Esta é a história de um jovem...",
            "authors": [author_create]
        }
        book_dict = custom_book or default_book_dict

        return BookCreate(**book_dict)

    return _to_model


@pytest.fixture
def book_create(callable_book_create):
    return callable_book_create()


@pytest.fixture
def create_book(db_session, callable_book_create):
    def create_fn(custom_book: dict = None) -> BookRead:
        schema_dump = callable_book_create(custom_book).model_dump()
        author_schema = schema_dump["authors"][0]
        author_model = Author(**author_schema)
        del schema_dump["authors"]

        book_model = Book(**schema_dump)
        book_model.authors = [author_model]
        db_session.add(book_model)
        db_session.commit()
        db_session.refresh(book_model)

        book_read = {
            **book_model.asdict(),
            "authors": [author_schema]
        }

        return BookRead(**book_read)

    return create_fn


def _fake_isbn() -> str:
    digits = [9, 7, 8]
    digits += [random.randint(0, 9) for _ in range(9)]

    total = sum((d if i % 2 == 0 else d * 3) for i, d in enumerate(digits))
    checksum = (10 - (total % 10)) % 10
    digits.append(checksum)

    return "".join(map(str, digits))


@pytest.fixture
def fetch_random_book() -> Callable:
    def _generate() -> dict:
        author_names = ["Guimarães", "Flaubert", "Michele", "Saramago", "Fernando"]
        author_descs = ["desc01", "desc02"]
        titles = ["Campo Geral", "Harry Potter", "Essencialismo"]
        publishers = ["pub01", "pub02"]
        categories = ["cat01", "cat02"]
        synopsis = ["syn01", "syn02"]

        return {
            "title": random.choice(titles),
            "publisher": random.choice(publishers),
            "isbn": _fake_isbn(),
            "category": random.choice(categories),
            "synopsis": random.choice(synopsis),
            "authors": [{
                "name": random.choice(author_names),
                "description": random.choice(author_descs)
            }]
        }

    return _generate


@pytest.fixture
def create_books(create_book, fetch_random_book):
    def _create(amount) -> list[BookRead]:

        books = []
        for _ in range(amount):
            books.append(create_book(fetch_random_book()))

        return books

    return _create
