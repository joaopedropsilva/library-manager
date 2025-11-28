from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.services.loan import LoanService


def get_loan_service(session: Session = Depends(get_session)) -> LoanService:
    return LoanService(session)
