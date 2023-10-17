from typing import TYPE_CHECKING
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel

from src.schemas.days_schema import IDayExpenseCreate, IDayExpenseDelete
from src.models.base import Base

from calendar import monthrange
import copy


if TYPE_CHECKING:
    from .user import User

    
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
    
    async def set_day_limit(self, day: int, limit: float) -> None:
        if str(day) not in self.days_statistics:
            raise Exception(f"There is no day number {day} in the month")
        
        self.days_statistics = copy.deepcopy(self.days_statistics)

        self.days_statistics[str(day)]["limit"] = limit
        self.days_statistics[str(day)]["money_rest"] = limit - self.days_statistics[str(day)]["total_expenses"]
        
        self.savings += self.days_statistics[str(day)]["savings_taken"]
        self.days_statistics[str(day)]["savings_taken"] = 0

    async def set_limits_after_day(self, begin_day: int, limit: float) -> None:
        if str(begin_day) not in self.days_statistics:
            raise Exception(f"There is no day number {begin_day} in the month")

        self.days_statistics = copy.deepcopy(self.days_statistics)
        for day in self.days_statistics:
            if int(day) >= begin_day:
                self.days_statistics[str(day)]["limit"] = limit
                self.days_statistics[str(day)]["money_rest"] = limit - self.days_statistics[str(day)]["total_expenses"]

                self.savings += self.days_statistics[str(day)]["savings_taken"]
                self.days_statistics[str(day)]["savings_taken"] = 0

    async def add_expense(self, day: int, expense: IDayExpenseCreate) -> None:
        self.days_statistics = copy.deepcopy(self.days_statistics)

        self.days_statistics[str(day)]["total_expenses"] += expense.cost
        self.days_statistics[str(day)]["money_rest"] -= expense.cost

        if expense.name not in self.days_statistics[str(day)]["expenses"]:
            self.days_statistics[str(day)]["expenses"][expense.name] = 0

        self.days_statistics[str(day)]["expenses"][expense.name] += expense.cost
        self.total_expenses += expense.cost

    async def delete_expense(self, day: int, expense: IDayExpenseDelete) -> None:
        if expense.name not in self.days_statistics[str(day)]["expenses"]:
            raise Exception(f"{expense.name} not found")
        
        self.days_statistics = copy.deepcopy(self.days_statistics)
        cost = self.days_statistics[str(day)]["expenses"][expense.name]

        self.days_statistics[str(day)]["total_expenses"] -= cost
        self.days_statistics[str(day)]["money_rest"] += cost
        del self.days_statistics[str(day)]["expenses"][expense.name]
        self.total_expenses -= cost

    async def transfer_to_savings(self, day: int, amount: float) -> None:
        if str(day) not in self.days_statistics:
            raise Exception(f"There is no day number {day} in the month")

        self.days_statistics = copy.deepcopy(self.days_statistics)
        if self.days_statistics[str(day)]["money_rest"] >= amount:
            self.days_statistics[str(day)]["money_rest"] -= amount
            self.days_statistics[str(day)]["savings_taken"] -= amount
            self.savings += amount
        else:
            raise Exception("The balance is less than the entered amount")

    async def transfer_from_savings(self, day: int, amount: float) -> None:
        if str(day) not in self.days_statistics:
            raise Exception(f"There is no day number {day} in the month")

        self.days_statistics = copy.deepcopy(self.days_statistics)

        if self.savings >= amount:
            self.savings -= amount
            self.days_statistics[str(day)]["savings_taken"] += amount
            self.days_statistics[str(day)]["money_rest"] += amount
        else:
            raise Exception("The savings is less than the entered amount")

    async def rest_to_savings(self, until_day: int) -> None:
        if str(until_day) not in self.days_statistics:
            raise Exception(f"There is no day number {day} in the month")

        self.days_statistics = copy.deepcopy(self.days_statistics)
        for day in self.days_statistics:
            if int(day) == until_day:
                return
            self.days_statistics[str(day)]["profit"] += self.days_statistics[str(day)]["money_rest"]

            self.savings += self.days_statistics[str(day)]["money_rest"]
            self.days_statistics[str(day)]["money_rest"] = 0

    async def rest_in_a_day(self, until_day: int) -> None:
        if str(until_day) not in self.days_statistics:
            raise Exception(f"There is no day number {day} in the month")
        
        self.days_statistics = copy.deepcopy(self.days_statistics)
        for day in self.days_statistics:
            if int(day) == until_day:
                return
            self.days_statistics[str(day)]["profit"] += self.days_statistics[str(day)]["money_rest"]

            self.days_statistics[str(until_day)]["money_rest"] += self.days_statistics[str(day)]["money_rest"] 
            self.days_statistics[str(until_day)]["limit"] += self.days_statistics[str(day)]["money_rest"]
            self.days_statistics[str(day)]["money_rest"] = 0

    async def is_limits_consistent(self, limits: dict[str, float]) -> dict:
        self.days_statistics = copy.deepcopy(self.days_statistics)

        # check sums
        old_sum_limit = sum([props["limit"] for day, props in self.days_statistics.items()])
        new_sum_limit = sum(limits.values())
        if old_sum_limit != new_sum_limit or len(self.days_statistics) != len(limits):
            raise Exception("Limits is incorrect")
        
        # check days
        for day in self.days_statistics:
            if str(day) not in limits:
                raise Exception(f"Day {str(day)} not specified")

        # recalculation of limits, money_rest
        for day in self.days_statistics:
            old_limit = self.days_statistics[str(day)]["limit"]
            self.days_statistics[str(day)]["money_rest"] += (limits[str(day)] - old_limit)
            self.days_statistics[str(day)]["limit"] = limits[str(day)]
    
        return self.days_statistics
