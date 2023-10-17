from typing import List
from sqlalchemy.sql import select

from src.repository.repositoryBase import SQLAlchemyRepository
from src.models.month import Month
from src.db.db import db


class MonthRepository(SQLAlchemyRepository):
    model = Month
    
    async def get_months(self, telegram_id: int) -> List[Month] | None:
        async with db.session_factory() as session:
           stmt = select(Month).where(Month.user_telegram_id==telegram_id)
           res = await session.execute(stmt)
           await session.commit()
           return res.scalars().all()

    async def get_month(self, telegram_id: int, month: int, year: int) -> Month | None:
        async with db.session_factory() as session:
           stmt = select(Month).where(
                Month.user_telegram_id==telegram_id,
                Month.month==month,
                Month.year==year
            )
           res = await session.execute(stmt)
           await session.commit()
           return res.scalar_one_or_none()
