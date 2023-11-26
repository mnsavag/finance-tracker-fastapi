from typing import Optional, TYPE_CHECKING
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


if TYPE_CHECKING:
    from src.user.data.models import User


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    month: Mapped[int]
    year: Mapped[int]

    month_stories: Mapped[dict] = mapped_column(JSON) 
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped[Optional["User"]] = relationship(back_populates="stories")
