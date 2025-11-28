from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.session import get_session
from api.db.models.book import Book
from api.services.book import BookService
from api.versions.v1.schema.author import AuthorCreate
from api.versions.v1.schema.book import BookRead


def get_book_service(session: Session = Depends(get_session)) -> BookService:
    return BookService(session)


def get_book_read_from_model(book: Book) -> BookRead:
    authors = []
    for author in book.authors:
        authors.append(
            AuthorCreate(
                name=author.name,
                description=author.description
            ).model_dump()
        )

    book_read = {
        **book.asdict(),
        "authors": authors
    }
    return BookRead(**book_read)
