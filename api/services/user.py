from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from api.db.models.user import User


class UserCreationException(Exception):
    def __init__(self, message: str):
        super().__init__(f"Failed to create user: {message}")


class UserService:
    def __init__(self, session: Session):
        self._db = session

    def create_user(self, name: str, phone: str, address: str, email: str) -> User:
        try:
            user = User(name=name, phone=phone, address=address, email=email)
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)
        except SQLAlchemyError as err:
            raise UserCreationException(err)

        return user
