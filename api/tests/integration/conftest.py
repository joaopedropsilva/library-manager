import random
import functools
import uuid
from typing import Generator

import pytest

from api.tests.integration.db import \
        db_eng, Base, db_session_override, User


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


def _user_seeder(db_session, amount):
    names = ["John", "Hugo", "Michele", "Nelson"]
    addresses = ["777 Fort Al St.- 85", "231 Reed St.- 22333", "255 Lincoln - 2"]
    email_mask = "example_{eid}@email.com"

    def _gen_phone():
        phone_mask = f"+55XXXXXXXXXXX"
        return "".join(
            str(random.randint(0, 9)) if ch == "X" else ch
            for ch in phone_mask
        )

    users = []
    for i in range(amount):
        eid = str(uuid.uuid4()).split("-")[0]
        email = email_mask.format(eid=eid)
        users.append(User(name=random.choice(names),
                          phone=_gen_phone(),
                          address= random.choice(addresses),
                          email=email))

    db_session.add_all(users)
    db_session.commit()


@pytest.fixture
def seed_db_with_users(db_session):
    return functools.partial(_user_seeder, db_session)
