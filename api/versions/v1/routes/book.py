from typing import Annotated

from fastapi import \
    APIRouter, Depends, status, HTTPException, Query

from api.services.book import \
    BookService, \
    BookCreationException, \
    BookAlreadyExistsException, \
    BookNotFoundException
from api.services.author import AuthorService, AuthorNotFoundException
from api.versions.v1.schema.book import BookCreate, BookRead
from api.versions.v1.dependencies.book import get_book_service
from api.versions.v1.dependencies.author import get_author_service
from api.services.pagination import paginate_response, MemoryPaginatedResponse


router = APIRouter()


@router.get("/books/")
def get_books():
    return []


@router.post("/books/", status_code=status.HTTP_201_CREATED)
def create_book(book: Annotated[dict, BookCreate],
                book_service: Annotated[BookService, Depends(get_book_service)],
                author_service: Annotated[AuthorService, Depends(get_author_service)]) -> BookRead:
    try:
        authors = author_service.get_authors_by_ids(book.author_ids)
    except AuthorNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        created_book = book_service.create_book(book.title,
                                           book.publisher,
                                           book.isbn,
                                           book.category,
                                           book.synopsis,
                                           authors)
        return BookRead(**created_book.asdict())
    except BookCreationException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except BookAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get("/books/availability/{book_id}")
def check_loan_availability(book_id: str):
    return True
