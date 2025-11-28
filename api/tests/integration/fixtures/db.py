from typing import Generator

import pytest

from api.tests.integration.db import db_eng, Base, db_session_override


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
