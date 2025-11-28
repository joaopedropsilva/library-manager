import uuid
import datetime

from pydantic import BaseModel, Field


class AuthorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None


class AuthorRead(AuthorCreate):
    id: uuid.UUID
    created_at: datetime.datetime
