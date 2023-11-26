from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.models import Base


if TYPE_CHECKING:
    from src.month.data.models import Month
    from src.history.data.models import History


class User(Base):
    __tablename__ = "user"

    telegram_id: Mapped[int] = mapped_column(default=None, primary_key=True)
    password: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    email: Mapped[Optional[str]] = mapped_column(nullable=True, index=True, unique=True)

    months: Mapped[List["Month"]] =  relationship(back_populates="user")
    stories: Mapped[List["History"]] = relationship(back_populates="user")
