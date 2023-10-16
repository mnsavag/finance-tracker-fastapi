import copy
from typing import List
from fastapi import HTTPException, status

from src.models.month import MonthBase, Month
from src.models.user import User
from src.repository.repositoryBase  import IRepositoryBase

from src.utils.time import get_date_by_time_zone, Date

from src.repository.month import MonthRepository
from src.repository.user import UserRepository
from src.schemas.days_schema import ISetLimit, IExpenseCreate, IExpenseDelete


class MonthService:
    month_repo: IRepositoryBase = MonthRepository()
    user_repo: IRepositoryBase = UserRepository()

    async def get_by_id(self, id) -> Month:
        return await self.month_repo.get(id)
    
    async def get_by_user_id_and_date(self, user_id: int, date: Date) -> Month | None:
        return await self.month_repo.get_month(user_id, date.month, date.year)
    
    async def get_current_month(self, user_id: int, date: Date):
        return await self.month_repo.get_month(user_id, date.month, date.year)
        
    async def add_month_to_user(self, month: Month, user: User):
        await self.is_unique_month(month, user.telegram_id)
        month.user_telegram_id = user.telegram_id
        await self.month_repo.create(dict(month))

    async def set_limits_after_day(self, month: Month, begin_day: int, limit: float) -> Month:
        await month.set_limits_after_day(begin_day, limit)
        return await self.month_repo.update(month)
    
    async def add_expense(self, month: Month, day: int, expense: IExpenseCreate) -> Month:
        await month.add_expense(day, expense)
        return await self.month_repo.update(month)
    
    async def delete_expense(self, month: Month, day: int, expense: IExpenseDelete) -> Month:
        await month.delete_expense(day, expense)
        return await self.month_repo.update(month)
    
    async def transfer_to_savings(self, month: Month, day: int, amount: float) -> Month:
        try:
            await month.transfer_to_savings(day, amount)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
        return await self.month_repo.update(month)
    
    async def transfer_from_savings(self, month: Month, day: int, amount: float) -> Month:
        try:
            await month.transfer_from_savings(day, amount)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
        return await self.month_repo.update(month)

    async def rest_to_savings(self, month: Month, until_day: int) -> Month:
        await month.rest_to_savings(until_day)
        return await self.month_repo.update(month)
    
    async def rest_in_a_day(self, month: Month, until_day: int) -> Month:
        await month.rest_in_a_day(until_day)
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
