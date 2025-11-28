import uuid
import datetime

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: PhoneNumber
    address: str = Field(min_length=10, max_length=120)
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "phone": "+5519999999999",
                "address": "344 Maranelo St.",
                "email": "john@doe.com"
            }
        }
    }


class UserRead(UserCreate):
    id: uuid.UUID
    phone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "292ada19-6b06-44f7-a20e-dc6687668b0e",
                "name": "John Doe",
                "phone": "+5519999999999",
                "address": "344 Maranelo St.",
                "email": "john@doe.com",
                "created_at": "2025-11-28T05:34:46.963Z",
                "updated_at": "2025-11-28T05:34:46.963Z"
            }
        }
    }
