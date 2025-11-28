from typing import Annotated

from fastapi import \
    APIRouter, Depends, status, HTTPException, Query, Path

from api.core.exceptions import UserMaxLoansExceededException, InvalidIdException
from api.services.loan import \
    LoanService, LoanCreationException, LoanNotFoundException, LoanReturnProcessException
from api.services.user import UserService, UserNotFoundException
from api.services.book import \
        BookService, BookNotFoundException, BookUnavailableException
from api.versions.v1.schema.loan import LoanCreate, LoanRead
from api.versions.v1.dependencies.user import get_user_service
from api.versions.v1.dependencies.book import get_book_service
from api.versions.v1.dependencies.loan import get_loan_service
from api.services.pagination import paginate_response, MemoryPaginatedResponse


router = APIRouter()


@router.get("/loans/", status_code=status.HTTP_200_OK, response_model=MemoryPaginatedResponse)
def get_loans(skip: Annotated[int, Query(description="Amount of loans to skip", ge=0)] = 0,
              limit: Annotated[int, Query(description="Amount of loans to get", ge=0, le=100)] = 10,
              active: Annotated[bool, Query(description="Lists only active loans")] = True,
              overdue: Annotated[bool, Query(description="Lists only overdue loans")] = False,
              service: Annotated[LoanService, Depends(get_loan_service)] = None) -> MemoryPaginatedResponse:
    loan_reads = [LoanRead(**loan.asdict()) for loan in service.get_all_loans(active, overdue)]
    return paginate_response(loan_reads, skip, limit)


@router.post("/loans/", status_code=status.HTTP_201_CREATED, response_model=LoanRead)
def create_loan(loan: LoanCreate,
                user_service: Annotated[UserService, Depends(get_user_service)],
                book_service: Annotated[BookService, Depends(get_book_service)],
                loan_service: Annotated[LoanService, Depends(get_loan_service)]) -> LoanRead:
    try:
        book = book_service.get_if_book_available(str(loan.book_id))
    except BookNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except BookUnavailableException as err:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail=str(err))

    try:
        user = user_service.get_user_by_id(str(loan.user_id))
        loan_service.check_if_max_loans_exceeded(user)
    except UserNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except UserMaxLoansExceededException as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(err))

    try:
        created_loan = loan_service.create_loan(book, user)
        return LoanRead(**created_loan.asdict())
    except LoanCreationException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


@router.post("/loans/return/{loan_id}", status_code=status.HTTP_200_OK, response_model=LoanRead)
def process_loan_return_with_fine(loan_id: Annotated[str, Path(description="Loan unique identifier (UUID4)")],
                                  service: Annotated[LoanService, Depends(get_loan_service)]) -> LoanRead:
    try:
        loan_processed = service.process_loan_return(loan_id)
        return LoanRead(**loan_processed.asdict())
    except LoanNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except LoanReturnProcessException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
