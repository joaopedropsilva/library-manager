from fastapi import APIRouter


router = APIRouter()


@router.get("/books/")
def get_books():
    return []


@router.post("/books/")
def create_book():
    return ""


@router.get("/books/availability/{book_id}")
def check_loan_availability(book_id: str):
    return True
