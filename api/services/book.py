import uuid
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

from api.core.exceptions import InvalidIdException
from api.db.models.book import Book
from api.db.models.author import Author


logger = logging.getLogger(__name__)


class BookCreationException(Exception):
    def __init__(self):
        super().__init__(f"Failed to create book")


class BookAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__(f"Book already exists")


class BookNotFoundException(Exception):
    def __init__(self):
        super().__init__(f"Book not found")


class BookUnavailableException(Exception):
    def __init__(self):
        super().__init__(f"Book is not available")


class BookService:
    def __init__(self, session: Session):
        self._db = session

    def get_all_books(self) -> list[Book]:
        stmt = select(Book)
        return self._db.scalars(stmt).all()

    def get_book_by_isbn(self, isbn: str) -> Book:
        stmt = select(Book).where(Book.isbn == isbn)
        book = self._db.scalars(stmt).first()
        if not book:
            raise BookNotFoundException()

        return book

    def create_book(self,
                    title: str,
                    publisher: str,
                    isbn: str,
                    category: str,
                    synopsis: str,
                    authors: list[Author]) -> Book:
        stmt = select(Book).where(Book.isbn == isbn)
        book = self._db.scalars(stmt).first()
        if book:
            raise BookAlreadyExistsException()

        try:
            book = Book(title=title,
                        publisher=publisher,
                        isbn=isbn,
                        category=category,
                        synopsis=synopsis,
                        authors=authors)
            self._db.add(book)
            self._db.commit()
            self._db.refresh(book)
        except SQLAlchemyError:
            logger.exception("Database failed to create book")
            raise BookCreationException()

        return book
