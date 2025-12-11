import datetime
from typing import Callable

import pytest

from api.versions.v1.schema.loan import LoanRead
from api.versions.v1.schema.book import BookRead
from api.versions.v1.schema.user import UserRead
from api.tests.db import Loan
from api.tests.config_defaults import settings


@pytest.fixture
def callable_loan_create(create_book, create_valid_user) -> Callable:
    def _create(book: dict = None, default_user_read: UserRead = None) -> tuple[BookRead, UserRead]:
        book_read = create_book(book)
        if not default_user_read:
            user_read = create_valid_user()

        return book_read, default_user_read or user_read

    return _create


@pytest.fixture
def loan_create(callable_loan_create) -> tuple[BookRead, UserRead]:
    return callable_loan_create()


@pytest.fixture
def create_loan(db_session, callable_loan_create) -> Callable:
    def _create(book: dict = None, default_user_read: UserRead = None) -> tuple[LoanRead, UserRead | None]:
        book_read, user_read = callable_loan_create(book, default_user_read)

        due_date_delta = datetime.timedelta(days=settings.default_loan_term_in_days)
        due_date = due_date_delta + datetime.datetime.now(datetime.timezone.utc)

        loan_model = Loan(book_id=book_read.id, user_id=user_read.id, due_date=due_date)
        db_session.add(loan_model)
        db_session.commit()
        db_session.refresh(loan_model)

        return LoanRead(**loan_model.asdict()), user_read

    return _create

@pytest.fixture
def create_loans(create_loan, fetch_random_book) -> Callable:
    def _create(loan_amount: int, default_user_read: UserRead = None) -> list[LoanRead]:
        loans = []

        user_read = default_user_read
        for _ in range(loan_amount):
            random_book = fetch_random_book()
            loan_read, user_read_from_loan = create_loan(random_book, user_read)
            if not user_read:
                user_read = user_read_from_loan

            loans.append(loan_read)

        return loans

    return _create
