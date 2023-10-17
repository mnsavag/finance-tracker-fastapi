from typing import List
from fastapi import HTTPException, status

from src.models.user import User
from src.models.month import Month
from src.repository.repositoryBase  import IRepositoryBase

from src.utils.time import Date

from src.repository.month import MonthRepository
from src.repository.user import UserRepository
from src.schemas.days_schema import IDayExpenseCreate, IDayExpenseDelete
from src.schemas.month_schema import IMonthCreate, IMonth, IMonthDefined


class MonthService:
    month_repo: IRepositoryBase = MonthRepository()
    user_repo: IRepositoryBase = UserRepository()

    async def get_by_id(self, id) -> IMonth:
        return await self.month_repo.get(id)
    
    async def get_month(self, user_id: int, date: Date) -> IMonth | None:
        return await self.month_repo.get_month(user_id, date.month, date.year)
    
    async def get_current_month(self, user_id: int, date: Date):
        return await self.month_repo.get_month(user_id, date.month, date.year)
        
    async def add_month_to_user(self, month_create: IMonthDefined, user: User):
        days: dict = await Month.get_init_stats(month_create.year, month_create.month)
        month: IMonthCreate = IMonthCreate(
            telegram_user_id = month_create.telegram_user_id,
            month = month_create.month,
            year = month_create.year,
            days_statistics = days 
        )
        await self.is_unique_month(month, user.telegram_id)
        await self.month_repo.create(dict(month))# вставить инициализацию статистики сюда

    async def set_day_limit(self, month: IMonthCreate, day: int, limit: float) -> IMonth:
        await month.set_day_limit(day, limit)
        return await self.month_repo.update(month)
    
    async def set_limits_after_day(self, month: IMonth, begin_day: int, limit: float) -> IMonth:
        await month.set_limits_after_day(begin_day, limit)
        return await self.month_repo.update(month)
    
    async def add_expense(self, month: IMonth, day: int, expense: IDayExpenseCreate) -> IMonth:
        await month.add_expense(day, expense)
        return await self.month_repo.update(month)
    
    async def delete_expense(self, month: IMonth, day: int, expense: IDayExpenseDelete) -> IMonth:
        await month.delete_expense(day, expense)
        return await self.month_repo.update(month)
    
    async def transfer_to_savings(self, month: IMonth, day: int, amount: float) -> IMonth:
        await month.transfer_to_savings(day, amount)
        return await self.month_repo.update(month)
    
    async def transfer_from_savings(self, month: IMonth, day: int, amount: float) -> IMonth:
        await month.transfer_from_savings(day, amount)
        return await self.month_repo.update(month)

    async def rest_to_savings(self, month: IMonth, until_day: int) -> IMonth:
        await month.rest_to_savings(until_day)
        return await self.month_repo.update(month)
    
    async def rest_in_a_day(self, month: IMonth, until_day: int) -> IMonth:
        await month.rest_in_a_day(until_day)
        return await self.month_repo.update(month)

    async def transfer_limits(self, month: IMonth, limits: dict[str, float]) -> None:
        await month.is_limits_consistent(limits)
        await self.month_repo.update(month)

    async def is_unique_month(self, month_in: IMonth, user_telegram_id: int) -> bool:
        months: List[IMonth] = await self.month_repo.get_months(user_telegram_id)
        for month in months:
            if month_in.month == month.month and month_in.year == month.year:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Month {month_in.month}.{month_in.year} for user already exists",
                )
        return True
