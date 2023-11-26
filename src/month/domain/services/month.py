from typing import List
from fastapi import HTTPException, status

from src.sql_alchemy_repository  import IRepositoryBase
from src.user.data.repositories.user import UserRepository
from src.month.data.repositories import MonthRepository

from src.month.data.models import Month
from src.user.data.models import User

from src.month.domain.schemas.date import Date
from src.month.domain.schemas.month import (
    MonthDefined, 
    MonthCreate
)


class MonthService:
    month_repo: IRepositoryBase = MonthRepository()
    user_repo: IRepositoryBase = UserRepository()

    async def get_by_id(self, id) -> Month:
        return await self.month_repo.get(id)
    
    async def get_month(self, user_id: int, date: Date) -> Month | None:
        return await self.month_repo.get_month(user_id, date.month, date.year)
    
    async def get_current_month(self, user_id: int, date: Date):
        return await self.month_repo.get_month(user_id, date.month, date.year)
        
    async def add_month_to_user(self, month_create: MonthDefined, user: User):
        days: dict = await Month.get_init_stats(month_create.year, month_create.month)
        month: MonthCreate = MonthCreate(
            telegram_user_id = month_create.telegram_user_id,
            month = month_create.month,
            year = month_create.year,
            days_statistics = days 
        )
        await self.is_unique_month(month, user.telegram_id)
        await self.month_repo.create(month)# вставить инициализацию статистики сюда

    async def is_unique_month(self, month_in: Month, user_telegram_id: int) -> bool:
        months: List[Month] = await self.month_repo.get_months(user_telegram_id)
        for month in months:
            if month_in.month == month.month and month_in.year == month.year:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Month {month_in.month}.{month_in.year} for user already exists",
                )
        return True
