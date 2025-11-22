from fastapi import APIRouter


router = APIRouter()


@router.get("/users/")
def get_users():
    return []


@router.post("/users/")
def create_user():
    return ""


@router.get("/users/{user_id}")
def get_user(user_id: str):
    return {"name": "John"}
