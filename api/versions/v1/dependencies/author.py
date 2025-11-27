from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.services.author import AuthorService


def get_author_service(session: Session = Depends(get_session)) -> AuthorService:
    return AuthorService(session)
