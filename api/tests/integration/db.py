from typing import Generator

import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from api.db.models.models import *


db_eng = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=db_eng)


def db_session_override() -> Generator[Session, None, None]:
    with _TestSession() as session:
        yield session
