from src.models import Base

from typing import TYPE_CHECKING
from pydantic import BaseModel
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from calendar import monthrange


if TYPE_CHECKING:
    from src.user.data.models import User

    
class IDayStats(BaseModel):
    limit: float
    money_rest: float
    profit: float # balance at the end of the day
    total_expenses: float
    savings_taken: float # > 0 => from month[savings] ||| < 0 => send to savings
    expenses: dict


class Month(Base):
    __tablename__ = "month"

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    user_telegram_id: Mapped[int]
    month: Mapped[int]
    year: Mapped[int]

    days_statistics: Mapped[dict] = mapped_column(JSON)
    total_expenses: Mapped[float] = mapped_column(default=0)
    savings: Mapped[float] = mapped_column(default=0)

    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('user.telegram_id'))
    user: Mapped["User"] = relationship(back_populates="months")
    

    @staticmethod
    async def get_init_stats(year: int, month: int) -> dict:
        days = monthrange(year, month)[1]
        statistic = {}
        for day in range(1, days + 1):
            statistic[day] = dict(IDayStats(
                                        limit=0, money_rest=0, profit=0,
                                        total_expenses=0, savings_taken=0, 
                                        expenses={}
                                    ))
        return statistic
