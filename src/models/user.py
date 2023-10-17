from typing import List, Optional, TYPE_CHECKING

from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .month import Month
    from .history import History


class UserBase(SQLModel):
    mail: Optional[EmailStr] = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )


class User(UserBase, table=True):
    __tablename__ = "user"

    telegram_id: Optional[int] = Field(default=None, primary_key=True)
    password: str | None = Field(nullable=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    months: List["Month"] | None =  Relationship(back_populates="user")
    stories: List["History"] | None = Relationship(back_populates="user")
