from typing import Annotated

from fastapi import \
    APIRouter, Depends, status, HTTPException, Query
from pydantic_extra_types.isbn import ISBN

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


@router.get("/books/", status_code=status.HTTP_200_OK)
def get_books(skip: Annotated[int, Query(title="Amount of books to skip", ge=0)] = 0,
              limit: Annotated[int, Query(title="Amount of books to get", ge=0, le=100)] = 10,
              service: Annotated[BookService, Depends(get_book_service)] = None) -> MemoryPaginatedResponse:
    books = [BookRead(**book.asdict()) for book in service.get_all_books()]
    return paginate_response(books, skip, limit)


@router.get("/books/{isbn}", status_code=status.HTTP_200_OK)
def get_book_by_isbn(isbn: Annotated[str, ISBN],
                     book_service: Annotated[BookService, Depends(get_book_service)],
                     author_service: Annotated[BookService, Depends(get_author_service)]) -> BookRead:
    book = book_service.get_book_by_isbn(isbn)
    if not book or not book.authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    book_read = book.asdict()
    del book["authors"]
    book_read["author_names"] = [a.name for a in book.authors]

    return BookRead(**book_read)


@router.post("/books/", status_code=status.HTTP_201_CREATED)
def create_book(book: Annotated[dict, BookCreate],
                book_service: Annotated[BookService, Depends(get_book_service)],
                author_service: Annotated[AuthorService, Depends(get_author_service)]) -> BookRead:
    try:
        authors = author_service.get_authors_by_ids(book.author_ids)
    except AuthorNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    author_ids = [a.id for a in authors]
    try:
        created_book = book_service.create_book(book.title,
                                           book.publisher,
                                           book.isbn,
                                           book.category,
                                           book.synopsis,
                                           authors)
        return BookRead({**created_book.asdict(), "author_ids": author_ids})
    except BookCreationException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except BookAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
