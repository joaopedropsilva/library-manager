import uuid
import datetime

from sqlalchemy import String, DateTime, Uuid, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
