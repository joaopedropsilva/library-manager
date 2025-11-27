import uuid
import datetime

from pydantic import BaseModel, Field
from pydantic_extra_types.isbn import ISBN


class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    publisher: str = Field(min_length=5, max_length=80)
    isbn: ISBN
    category: str | None = Field(min_length=5, max_length=30)
    synopsis: str | None
    author_ids: list[str] = Field(min_length=1)


class BookRead(BookCreate):
    id: uuid.UUID
    is_available: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author_names: list[str] | None = []
