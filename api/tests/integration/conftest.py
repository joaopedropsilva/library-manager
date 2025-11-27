import random
import datetime
import functools
import uuid
from typing import Generator

import pytest
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from api.versions.v1.schema.user import UserCreate, UserRead
from api.versions.v1.schema.book import BookCreate, BookRead
from api.versions.v1.schema.author import AuthorCreate, AuthorRead
from api.tests.integration.db import \
        db_eng, Base, db_session_override, User, Book


# Global definitions

@pytest.fixture(scope="session")
def engine():
    return db_eng


@pytest.fixture(scope="session")
def base():
    return Base


@pytest.fixture(autouse=True)
def clear_db(base, engine) -> Generator[None, None, None]:
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)
    yield
    base.metadata.drop_all(engine)


@pytest.fixture
def db_session():
    return next(db_session_override())


def _create_valid(db_session: Session,
                  create_schema: BaseModel,
                  read_schema: BaseModel,
                  db_model: Base) -> BaseModel:
    schema_dump = create_schema.model_dump()
    # Prevent passing down undeclared columns to db_model
    model_cols = set([c.name for c in inspect(db_model).columns])
    allowed_schema = {k: v for k, v in schema_dump.items() if k in model_cols}

    model = db_model(**allowed_schema)
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)

    mocked_read_result = model.asdict()
    # Reinsert dependencies removed
    mocked_read_result = {**mocked_read_result, **schema_dump}

    return read_schema(**mocked_read_result)


# User fixtures

@pytest.fixture
def seed_db_with_users(db_session):
    def _user_seeder(db_session, amount):
        names = ["John", "Hugo", "Michele", "Nelson"]
        addresses = ["777 Fort Al St.- 85", "231 Reed St.- 22333", "255 Lincoln - 2"]
        email_mask = "example_{eid}@email.com"

        users = []
        for i in range(amount):
            eid = str(uuid.uuid4()).split("-")[0]
            email = email_mask.format(eid=eid)
            user_schema = UserCreate(
                name=random.choice(names),
                phone="+5519999999999",
                address=random.choice(addresses),
                email=email
            )
            users.append(User(**user_schema.model_dump()))

        db_session.add_all(users)
        db_session.commit()

    return functools.partial(_user_seeder, db_session)


@pytest.fixture
def user() -> UserCreate:
    user_dict = {
        "name": "John",
        "phone": "+5519999999999",
        "address": "255 Lincoln Av.",
        "email": "john@doe.com"
    }

    return UserCreate(**user_dict)


@pytest.fixture
def create_valid_user(db_session, user) -> UserRead:
    def _create_valid():
        user_model = User(**user.model_dump())
        db_session.add(user_model)
        db_session.commit()
        db_session.refresh(user_model)

        return UserRead(**user_model.asdict())

    return _create_valid


# Author fixtures

@pytest.fixture
def author() -> AuthorCreate:
    author_dict = {
        "name": "Fernando Sabino",
        "description": "Autor mineiro"
    }

    return AuthorCreate(**author_dict)


@pytest.fixture
def create_valid_author(db_session, author) -> AuthorRead:
    create_fn = functools.partial(_create_valid,
                                  db_session,
                                  author,
                                  AuthorRead,
                                  Author)
    return create_fn()


# Book fixtures

@pytest.fixture
def book() -> BookCreate:
    book_dict = {
        "title": "O Encontro Marcado",
        "publisher": "Record",
        "isbn": "9788501912008",
        "category": "literature",
        "synopsis": "Esta é a história de um jovem...",
        "author_ids": [str(uuid.uuid4())]
    }

    return BookCreate(**book_dict)


@pytest.fixture
def create_book(db_session, book) -> BookRead:
    # create author here
    create_fn = functools.partial(_create_valid,
                                  db_session,
                                  book,
                                  BookRead,
                                  Book)
    return create_fn
