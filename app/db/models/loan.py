import uuid
import datetime

from sqlalchemy import Float, DateTime, Uuid, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Loan(Base):
    __tablename__ = "loan"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4())
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    due_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    return_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    fine: Mapped[float] = mapped_column(Float, default=0.0)
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
