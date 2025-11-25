from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.services.user import UserService


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)
