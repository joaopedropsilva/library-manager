import uuid
import datetime
from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: PhoneNumber
    address: str = Field(min_length=10, max_length=120)
    email: EmailStr


class UserRead(UserCreate):
    id: uuid.UUID
    phone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
