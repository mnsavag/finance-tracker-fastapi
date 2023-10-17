from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from src.models.base import Base

if TYPE_CHECKING:
    from .month import Month
    from .history import History


class User(Base):
    __tablename__ = "user"

    telegram_id: Mapped[int] = mapped_column(default=None, primary_key=True)
    password: Mapped[Optional[str]] = mapped_column(nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    mail: Mapped[Optional[str]] = mapped_column(nullable=True, index=True, unique=True)

    months: Mapped[List["Month"]] =  relationship(back_populates="user")
    stories: Mapped[List["History"]] = relationship(back_populates="user")
