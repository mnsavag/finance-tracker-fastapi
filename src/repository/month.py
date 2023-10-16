import copy
from sqlalchemy import update
from src.db.db import db
from src.models.month import MonthBase
from src.models.month import Month

from sqlalchemy.sql import select
from src.utils.time import Date
from typing import List
from src.repository.repositoryBase import SQLAlchemyRepository
import json
from sqlalchemy.orm import attributes


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
