from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import Base

author_book = Table(
    "autor_book",
    Base.metadata,
    Column("author_id", ForeignKey("author.id")),
    Column("book_id", ForeignKey("book.id"))
)
