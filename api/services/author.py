import uuid
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from api.db.models.author import Author


logger = logging.getLogger(__name__)


class AuthorCreationException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(f"Failed to create author")


class AuthorAlreadyExistsException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(f"Author already exists")


class AuthorNotFoundException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(f"Author not found")


class AuthorService:
    def __init__(self, session: Session):
        self._db = session

    def get_all_authors(self) -> list[Author]:
        stmt = select(Author)

        return self._db.scalars(stmt).all()

    def get_author_by_id(self, author_id: str) -> Author:
        try:
            author_uuid = uuid.UUID(author_id)
        except ValueError:
            raise AuthorNotFoundException()

        stmt = select(Author).where(Author.id == author_uuid)
        author = self._db.scalars(stmt).first()
        if not author:
            raise AuthorNotFoundException()

        return author

    def get_author_by_name(self, name: str) -> Author:
        stmt = select(Author).where(Author.name == name)

        return self._db.scalars(stmt).first()

    def create_author(self, name: str, description: str) -> Author:
        author = self.get_author_by_name(name)
        if author:
            raise AuthorAlreadyExistsException()

        try:
            author = Author(name=name, description=description)
            self._db.add(author)
            self._db.commit()
            self._db.refresh(author)
        except SQLAlchemyError:
            logger.exception("Database failed to create author")
            raise AuthorCreationException

        return author

    def get_authors_by_ids(self, author_ids: list[str]) -> list[Author]:
        normalized_author_ids = []
        for aid in author_ids:
            try:
                normalized_author_ids.append(uuid.UUID(aid))
            except ValueError:
                raise AuthorNotFoundException()

        stmt = select(Author).where(Author.id.in_(normalized_author_ids))

        return self._db.scalars(stmt).all()
