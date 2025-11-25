from typing import Generator

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from api.db.models.base import Base
from api.db.models.user import User
from api.db.models.loan import Loan
from api.db.models.book import Book
from api.db.models.author import Author


_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def db_session() -> Generator[Session, None, None]:
    with _TestSession() as session:
        yield session


@pytest.fixture(autouse=True)
def clear_db() -> Generator[Session, None, None]:
    Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)
    yield
    Base.metadata.drop_all(_engine)
