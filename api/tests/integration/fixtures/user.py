import random
import functools
import uuid

import pytest

from api.versions.v1.schema.user import UserCreate, UserRead
from api.tests.integration.db import User


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
def create_valid_user(db_session, user):
    def _create_valid():
        user_model = User(**user.model_dump())
        db_session.add(user_model)
        db_session.commit()
        db_session.refresh(user_model)

        return UserRead(**user_model.asdict())

    return _create_valid


@pytest.fixture
def seed_db_with_users(db_session):
    def _user_seeder(db_session, amount):
        names = ["John", "Hugo", "Michele", "Nelson"]
        addresses = ["777 Fort Al St.- 85", "231 Reed St.- 22333", "255 Lincoln - 2"]
        email_mask = "example_{eid}@email.com"

        users = []
        for _ in range(amount):
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
