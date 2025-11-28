from typing import Annotated

from fastapi import \
    APIRouter, Depends, status, HTTPException, Query

from api.services.user import \
    UserService, \
    UserCreationException, \
    UserAlreadyExistsException, \
    UserNotFoundException
from api.versions.v1.schema.user import UserCreate, UserRead
from api.versions.v1.dependencies.user import get_user_service
from api.services.pagination import paginate_response, MemoryPaginatedResponse


router = APIRouter()


@router.get("/users/", status_code=status.HTTP_200_OK)
def get_users(skip: Annotated[int, Query(title="Amount of users to skip", ge=0)] = 0,
              limit: Annotated[int, Query(title="Amount of users to get", ge=0, le=100)] = 10,
              service: Annotated[UserService, Depends(get_user_service)] = None) -> MemoryPaginatedResponse:
    users = [UserRead(**user.asdict()) for user in service.get_all_users()]
    return paginate_response(users, skip, limit)


@router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate,
                service: Annotated[UserService, Depends(get_user_service)]) -> UserRead:
    try:
        created_user = service.create_user(user.name, user.phone, user.address, user.email)
        return UserRead(**created_user.asdict())
    except UserCreationException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except UserAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: str, service: Annotated[str, Depends(get_user_service)]) -> UserRead:
    try:
        user = service.get_user_by_id(user_id)
        return UserRead(**user.asdict())
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
