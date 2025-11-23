from fastapi import APIRouter


router = APIRouter()


@router.get("/loans/{user_id}")
def get_loans_by_user(user_id: str):
    return []


@router.get("/loans/history/{user_id}")
def get_loan_history_by_user(user_id: str):
    return []


@router.get("/loans/active/")
def get_active_loans():
    return []


@router.get("/loans/overdue/")
def get_overdue_loans():
    return []


@router.post("/loans/")
def create_loan():
    return ""


@router.post("/loans/return/{loan_id}")
def process_loan_return_with_fine(loand_id: str):
    return ""
