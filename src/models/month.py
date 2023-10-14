from typing import Dict, List, Optional, TYPE_CHECKING
from pydantic import validator
from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field, Relationship
import pytz
from datetime import datetime
from calendar import monthrange
from src.utils.time import get_data_by_time_zone, Data
import json

if TYPE_CHECKING:
    from .user import User


class IDayStats(SQLModel):
    limit: float
    money_rest: float
    total_expenses: float
    savings: float
    expenses: dict


class MonthBase(SQLModel):
    user_telegram_id: int
    time_zone: str

    @validator("time_zone")
    def is_valid_time_zone(cls, time_zone):
      valid_zones = pytz.all_timezones
      if time_zone not in valid_zones:
        raise ValueError(f'The time zone indicated is incorrect {time_zone}')
      return time_zone


class Month(MonthBase, table=True):
    __tablename__ = "month"

    id: Optional[int] = Field(default=None, primary_key=True)
    day: int
    month: int
    year: int

    days_statistics: Dict = Field(default={}, sa_column=Column(JSON)) 
    total_expenses: float = Field(default=0)
    savings: float = Field(default=0)

    user_telegram_id: int = Field(foreign_key=('user.telegram_id'))
    user: Optional["User"] = Relationship(back_populates="months")
    
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    async def get_init_month(cls, time_zone: str):
        data: Data = await get_data_by_time_zone(time_zone)
        statistic: dict = await Month.get_init_stats(data)
        return cls(
            time_zone=time_zone,
            day=data.day, 
            month=data.month, 
            year=data.year, 
            days_statistics=statistic,
        )

    @classmethod
    async def get_init_stats(cls, data: Data) -> dict:
        days = monthrange(data.year, data.month)[1]
        statistic = {}
        for day in range(1, days + 1):
            statistic[day] = dict(IDayStats(
                                        limit=0, money_rest=0, 
                                        total_expenses=0, savings=0, expenses={}
                                    ))
        return statistic
