from typing import Annotated

from fastapi import \
    APIRouter, Depends, status, HTTPException, Query, Path

from api.core.exceptions import InvalidIdException
from api.services.loan import LoanService
from api.services.user import \
    UserService, \
    UserCreationException, \
    UserAlreadyExistsException, \
    UserNotFoundException
from api.services.pagination import paginate_response, MemoryPaginatedResponse
from api.versions.v1.schema.user import UserCreate, UserRead
from api.versions.v1.schema.loan import LoanRead
from api.versions.v1.dependencies.user import get_user_service
from api.versions.v1.dependencies.loan import get_loan_service


router = APIRouter()


@router.get("/users/", status_code=status.HTTP_200_OK, response_model=MemoryPaginatedResponse)
def get_users(skip: Annotated[int, Query(description="Amount of users to skip", ge=0)] = 0,
              limit: Annotated[int, Query(description="Amount of users to get", ge=0, le=100)] = 10,
              service: Annotated[UserService, Depends(get_user_service)] = None) -> MemoryPaginatedResponse:
    users = [UserRead(**user.asdict()) for user in service.get_all_users()]
    return paginate_response(users, skip, limit)


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user(user: UserCreate,
                service: Annotated[UserService, Depends(get_user_service)]) -> UserRead:
    try:
        created_user = service.create_user(user.name, user.phone, user.address, user.email)
        return UserRead(**created_user.asdict())
    except UserCreationException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    except UserAlreadyExistsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user(user_id: Annotated[str, Path(description="User unique identifier (UUID4)")],
             service: Annotated[UserService, Depends(get_user_service)]) -> UserRead:
    try:
        user = service.get_user_by_id(user_id)
        return UserRead(**user.asdict())
    except UserNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get("/users/loans/{user_id}", status_code=status.HTTP_200_OK, response_model=MemoryPaginatedResponse)
def get_loan_history_by_user(user_id: Annotated[str, Path(description="User unique identifier (UUID4)")],
                             skip: Annotated[int, Query(description="Amount of loans to skip", ge=0)] = 0,
                             limit: Annotated[int, Query(description="Amount of loans to get", ge=0, le=100)] = 10,
                             loan_service: Annotated[LoanService, Depends(get_loan_service)] = None) -> MemoryPaginatedResponse:
    try:
        loan_reads = [LoanRead(**loan.asdict()) for loan in loan_service.get_loans_by_user(user_id)]
        return paginate_response(loan_reads, skip, limit)
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
@router.get("/users/loans/{user_id}", status_code=status.HTTP_200_OK, response_model=MemoryPaginatedResponse)
def get_loan_history_by_user(user_id: Annotated[str, Path(description="User unique identifier (UUID4)")],
                             skip: Annotated[int, Query(description="Amount of loans to skip", ge=0)] = 0,
                             limit: Annotated[int, Query(description="Amount of loans to get", ge=0, le=100)] = 10,
                             loan_service: Annotated[LoanService, Depends(get_loan_service)] = None) -> MemoryPaginatedResponse:
    try:
        loan_reads = [LoanRead(**loan.asdict()) for loan in loan_service.get_loans_by_user(user_id)]
        return paginate_response(loan_reads, skip, limit)
    except InvalidIdException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
