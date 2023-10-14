import copy
from typing import List
from fastapi import HTTPException, status

from src.models.month import MonthBase, Month
from src.models.user import User
from src.repository.repositoryBase  import IRepositoryBase

from src.utils.time import get_data_by_time_zone, Data
from src.utils.exceptions.common import NotFoundException
from src.utils.exceptions.user import UserNotFoundException
from src.utils.exceptions.month import MonthNotFoundException

from src.repository.month import MonthRepository
from src.repository.user import UserRepository
from src.schemas.days_schema import ISetLimit, IExpenseCreate, IExpenseDelete


class MonthService:
    month_repo: IRepositoryBase = MonthRepository()
    user_repo: IRepositoryBase = UserRepository()

    async def get_by_id(self, id) -> Month:
        return await self.month_repo.get(id)
    
    async def get_by_user_id_and_data(self, user_id: int, data: Data) -> Month | None:
        return await self.month_repo.get_month(user_id, data.month, data.year)
    
    async def get_current_month(self, user_id: int, data: Data):
        return await self.month_repo.get_month(user_id, data.month, data.year)
        
    async def add_month_to_user(self, month: Month, user: User):
        await self.is_unique_month(month, user.telegram_id)
        month.user_telegram_id = user.telegram_id
        await self.month_repo.create(dict(month))

    async def set_limits_after_day(self, month: Month, begin_day: int, limit: float) -> dict:
        month.days_statistics = copy.deepcopy(month.days_statistics)
        for day in month.days_statistics:
            if int(day) >= begin_day:
                month.days_statistics[str(day)]["limit"] = limit
                month.days_statistics[str(day)]["money_rest"] = limit - month.days_statistics[str(day)]["total_expenses"] - month.days_statistics[str(day)]["savings"]
        return await self.month_repo.update(month)
    
    async def add_expense(self, month: Month, day: int, expense: IExpenseCreate) -> Month:
        month.days_statistics = copy.deepcopy(month.days_statistics)

        month.days_statistics[str(day)]["total_expenses"] += expense.cost
        month.days_statistics[str(day)]["money_rest"] -= expense.cost

        if expense.name not in month.days_statistics[str(day)]["expenses"]:
            month.days_statistics[str(day)]["expenses"][expense.name] = 0

        month.days_statistics[str(day)]["expenses"][expense.name] += expense.cost
        month.total_expenses += expense.cost
        return await self.month_repo.update(month)
    
    async def delete_expense(self, month: Month, day: int, expense: IExpenseDelete) -> Month:
        month.days_statistics = copy.deepcopy(month.days_statistics)
        cost = month.days_statistics[str(day)]["expenses"][expense.name]

        month.days_statistics[str(day)]["total_expenses"] -= cost
        month.days_statistics[str(day)]["money_rest"] += cost
        del month.days_statistics[str(day)]["expenses"][expense.name]
        month.total_expenses -= cost
        return await self.month_repo.update(month)
    
    async def transfer_to_savings(self, month: Month, day: int, amount: float) -> Month:
        month.days_statistics = copy.deepcopy(month.days_statistics)
        if month.days_statistics[str(day)]["money_rest"] >= amount:
            month.days_statistics[str(day)]["money_rest"] -= amount

            month.days_statistics[str(day)]["savings"] += amount
            month.savings += amount
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"The balance is less than the entered amount",
            )
        return await self.month_repo.update(month)
    
    async def transfer_from_savings(self, month: Month, day: int, amount: float) -> Month:
        month.days_statistics = copy.deepcopy(month.days_statistics)
        if month.savings >= amount:
            month.savings -= amount
            if month.days_statistics[str(day)]["savings"] >= amount:
                month.days_statistics[str(day)]["savings"] -= amount
            else:
                month.days_statistics[str(day)]["savings"] = 0
            month.days_statistics[str(day)]["money_rest"] += amount
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"The savings is less than the entered amount",
            )
        return await self.month_repo.update(month)

    async def is_unique_month(self, month_in: MonthBase, user_telegram_id: int) -> bool:
        months: List[Month] = await self.month_repo.get_months(user_telegram_id)
        for month in months:
            if month_in.month == month.month and month_in.year == month.year:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Month {month_in.month}.{month_in.year} for user already exists",
                )
        return True
