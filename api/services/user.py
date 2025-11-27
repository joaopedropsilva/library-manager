import uuid
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from api.db.models.user import User


logger = logging.getLogger(__name__)


class UserCreationException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(f"Failed to create user")


class UserAlreadyExistsException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(f"User already exists")


class UserNotFoundException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(f"User not found")


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def get_all_users(self) -> list[User]:
        stmt = select(User)

        return self._db.scalars(stmt).all()

    def get_user_by_id(self, user_id: str) -> User:
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise UserNotFoundException()

        stmt = select(User).where(User.id == user_uuid)
        user = self._db.scalars(stmt).first()
        if not user:
            raise UserNotFoundException()

        return user

    def get_user_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)

        return self._db.scalars(stmt).first()

    def create_user(self, name: str, phone: str, address: str, email: str) -> User:
        user = self.get_user_by_email(email)
        if user:
            raise UserAlreadyExistsException()

        try:
            user = User(name=name, phone=phone, address=address, email=email)
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)
        except SQLAlchemyError:
            logger.exception("Database failed to create user")
            raise UserCreationException()

        return user
