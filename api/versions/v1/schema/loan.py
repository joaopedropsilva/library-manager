import uuid
import datetime

from pydantic import BaseModel, Field


class LoanRead(BaseModel):
    id: uuid.UUID
    is_active: bool
    due_date: datetime.datetime
    return_date: datetime.datetime | None
    fine: float = Field(ge=0)
    created_at: datetime.datetime
    updated_at: datetime.datetime

    book_id: uuid.UUID
    user_id: uuid.UUID

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "292ada19-6b06-44f7-a20e-dc6687668b0e",
                "return_date": "2025-11-29T05:34:46.963Z",
                "fine": 0.0,
                "created_at": "2025-11-28T05:34:46.963Z",
                "updated_at": "2025-11-28T05:34:46.963Z",
                "book_id": "292ada19-6b06-44f7-a20e-dc6687668b0e",
                "user_id": "292ada19-6b06-44f7-a20e-dc6687668b0e"
            }
        }
    }
