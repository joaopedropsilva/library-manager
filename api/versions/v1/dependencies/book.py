from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.services.book import BookService


def get_book_service(session: Session = Depends(get_session)) -> BookService:
    return BookService(session)
