import uuid
import datetime
import logging

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from api.core.config import settings
from api.core.exceptions import InvalidIdException, UserMaxLoansExceededException
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

        loans = self._db.scalars(stmt).all()
        if not overdue:
            return loans

        loans_overdue = []
        for l in loans:
            if l.return_date and l.return_date > l.due_date:
                loans_overdue.append(l)
                continue

            time_delta = l.return_date - datetime.datetime.now(datetime.timezone.utc)
            if time_delta.days > settings.default_loan_term_in_days:
                loans_overdue.append(l)

        return loans_overdue

    def get_loans_by_user(self, user_id: str) -> list[Loan]:
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise InvalidIdException()

        stmt = select(Loan).where(Loan.user_id == user_uuid)
        loans = self._db.scalars(stmt).all()
        if not loans:
            raise LoanNotFoundException()

        return loans

    def process_loan_return(self, loan_id: str) -> Loan:
        try:
            loan_uuid = uuid.UUID(loan_id)
        except ValueError:
            raise InvalidIdException()

        stmt = select(Loan).where(Loan.id == loan_uuid)
        loan = self._db.scalars(stmt).first()

        if not loan:
            raise LoanNotFoundException()

        return_date_computed = datetime.datetime.now(datetime.timezone.utc)
        period = return_date_computed - loan.due_date
        days_overdue = period.days - settings.default_loan_term_in_days
        fine = days_overdue * settings.fine_amount_per_day

        loan.fine = fine
        try:
            stmt = update(Loan).where(Loan.id == loan.id).values(fine=fine).returning(Loan)
            result = self._db.execute(stmt)
            self._db.commit()
            return result.scalar_one()
        except SQLAlchemyError:
            logger.exception("Database failed to process loan")
            raise LoanReturnProcessException()

    def check_if_max_loans_exceeded(self, user: User) -> None:
        try:
            loans = self.get_loans_by_user(str(user.id))
        except LoanNotFoundException:
            return

        if len(loans) > settings.max_active_loans_per_user:
            raise UserMaxLoansExceededException()

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
            raise LoanCreationException()

        return loan
