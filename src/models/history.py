from typing import Dict, Optional, TYPE_CHECKING
from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class History(SQLModel, table=True):
    __tablename__ = "history"

    id: Optional[int] = Field(default=None, primary_key=True)
    month: int
    year: int

    month_stories: Dict = Field(default={}, sa_column=Column(JSON))
    user_telegram_id: int = Field(foreign_key=('user.telegram_id'))
    user: Optional["User"] = Relationship(back_populates="stories")

    class Config:
        arbitrary_types_allowed = True
