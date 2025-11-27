import uuid
import datetime

from pydantic import BaseModel, Field

from api.versions.v1.schema.book import BookRead 


class AuthorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None


class AuthorRead(AuthorCreate):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    books: list[BookRead] | None = []
