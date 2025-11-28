from typing import Annotated

from fastapi import \
    APIRouter, Depends, status, HTTPException, Query, Path
from pydantic_extra_types.isbn import ISBN

from api.services.book import \
    BookService, \
    BookCreationException, \
    BookNotFoundException, \
    BookAlreadyExistsException
from api.versions.v1.schema.book import BookCreate, BookRead
from api.db.models.author import Author
from api.versions.v1.dependencies.book import get_book_service, get_book_read_from_model
from api.services.pagination import paginate_response, MemoryPaginatedResponse


router = APIRouter()


@router.get("/books/", status_code=status.HTTP_200_OK, response_model=MemoryPaginatedResponse)
def get_books(skip: Annotated[int, Query(description="Amount of books to skip", ge=0)] = 0,
              limit: Annotated[int, Query(description="Amount of books to get", ge=0, le=100)] = 10,
              service: Annotated[BookService, Depends(get_book_service)] = None) -> MemoryPaginatedResponse:
    book_reads = [get_book_read_from_model(book) for book in service.get_all_books()]
    return paginate_response(book_reads, skip, limit)


@router.get("/books/{isbn}", status_code=status.HTTP_200_OK, response_model=BookRead)
def get_book_by_isbn(isbn: Annotated[ISBN, Path(description="Book identifier (ISBN)")],
                     book_service: Annotated[BookService, Depends(get_book_service)]) -> BookRead:
    try:
        book = book_service.get_book_by_isbn(isbn)
    except BookNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return get_book_read_from_model(book)


@router.post("/books/", status_code=status.HTTP_201_CREATED, response_model=BookRead)
def create_book(book: BookCreate,
                book_service: Annotated[BookService, Depends(get_book_service)]) -> BookRead:
    try:
        authors = []
        for author in book.authors:
            authors.append(Author(**author.model_dump()))

        created_book = book_service.create_book(book.title,
                                                book.publisher,
                                                book.isbn,
                                                book.category,
                                                book.synopsis,
                                                authors)
        return get_book_read_from_model(created_book)
    except BookCreationException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except BookAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
