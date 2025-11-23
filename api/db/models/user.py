import uuid
import datetime
from typing import List

from sqlalchemy import String, Uuid, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)

    # email size recommendation
    # https://stackoverflow.com/a/1199238
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
        onupdate=func.now()
    )

    loans: Mapped[List["Loan"]] = relationship(back_populates="user")
