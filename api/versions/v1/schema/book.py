import uuid
import datetime

from pydantic import BaseModel, Field
from pydantic_extra_types.isbn import ISBN

from api.versions.v1.schema.author import AuthorCreate


class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    publisher: str = Field(min_length=5, max_length=80)
    isbn: ISBN
    category: str | None = Field(min_length=5, max_length=30)
    synopsis: str | None
    authors: list[AuthorCreate] = Field(min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Harry Potter",
                "publisher": "Bloomsbury Publishing",
                "isbn": "9788532511010",
                "category": "fiction",
                "is_available": True,
                "synopsis": "The book synopsis",
                "authors": [{
                    "name": "J. K. Rowling",
                    "description": "The author description",
                }]
            }
        }
    }


class BookRead(BookCreate):
    id: uuid.UUID
    is_available: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "292ada19-6b06-44f7-a20e-dc6687668b0e",
                "title": "Harry Potter",
                "publisher": "Bloomsbury Publishing",
                "isbn": "9788532511010",
                "category": "fiction",
                "is_available": True,
                "synopsis": "The book synopsis",
                "authors": [{
                    "name": "J. K. Rowling",
                    "description": "The author description",
                }],
                "created_at": "2025-11-28T05:34:46.963Z",
                "updated_at": "2025-11-28T05:34:46.963Z"
            }
        }
    }
