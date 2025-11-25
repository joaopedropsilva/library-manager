from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from api.services.user import UserService, UserCreationException
from api.versions.v1.schema.user import UserCreate
from api.versions.v1.dependencies.user import get_user_service


router = APIRouter()


@router.get("/users/")
def get_users():
    return []


@router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: Annotated[dict, UserCreate],
                service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return service.create_user(user.name, user.phone, user.address, user.email)
    except UserCreationException as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=repr(err))


@router.get("/users/{user_id}")
def get_user(user_id: str):
    return {"name": "John"}
