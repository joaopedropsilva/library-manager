import uuid
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from api.core.exceptions import InvalidIdException
from api.db.models.loan import Loan
from api.db.models.book import Book
from api.db.models.user import User


logger = logging.getLogger(__name__)


class LoanCreationException(Exception):
    def __init__(self):
        super().__init__(f"Failed to create loan")


class LoanNotFoundException(Exception):
    def __init__(self):
        super().__init__(f"Loan(s) not found")


class LoanReturnProcessException(Exception):
    def __init__(self):
        super().__init__(f"Unable to process Loan return")


class LoanService:
    def __init__(self, session: Session):
        self._db = session

    def get_all_loans(self, active: bool, overdue: bool) -> list[Loan]:
        stmt = select(Loan)
        if active:
            stmt = select(Loan).where(Loan.is_active)
        return self._db.scalars(stmt).all()

    def get_loans_by_user(self, user_id: str) -> list[Loan]:
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise InvalidIdException

        stmt = select(Loan).where(Loan.user_id == user_uuid)
        loans = self._db.scalars(stmt).all()
        if not loans:
            raise LoanNotFoundException

        return loans

    def create_loan(self, book: Book, user: User) -> Loan:
        try:
            loan = Loan(book_id=book.id, user_id=user.id)
            loan.book = book
            loan.user = user
            self._db.add(loan)
            self._db.commit()
            self._db.refresh(loan)
        except SQLAlchemyError:
            logger.exception("Database failed to create loan")
            raise LoanCreationException

        return loan
