from typing import Callable

import pytest

from api.versions.v1.schema.loan import LoanRead
from api.tests.fixtures.book import create_book
from api.tests.fixtures.user import create_valid_user


@pytest.fixture
def callable_loan_parts(create_book, create_valid_user) -> Callable:
    def _create() -> tuple[str, str]:
        book = create_book()
        user = create_valid_user()

        return str(book.id), str(user.id)

    return _create


@pytest.fixture
def loan_parts(callable_loan_parts):
    return callable_loan_parts()
