import uuid
import datetime

from pydantic import BaseModel, Field


class AuthorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Fernando Sabino",
                "description": "Brazilian author"
            }
        }
    }


class AuthorRead(AuthorCreate):
    id: uuid.UUID
    created_at: datetime.datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "292ada19-6b06-44f7-a20e-dc6687668b0e",
                "name": "Fernando Sabino",
                "description": "Brazilian author",
                "created_at": "2025-11-28T05:34:46.963Z"
            }
        }
    }
