from typing import Dict
from sqlmodel import SQLModel
from src.models.month import MonthBase
from src.schemas.date_scheme import DateFull, DateMonthYear


class ISpecificMonth(DateMonthYear):
    user_id: int


class ISpecificDate(DateFull):
    user_id: int

class ITransferSavings(DateFull):
    user_id: int
    amount: int


#class IDayStats(SQLModel):
#    limit: float
#    money_rest: float
#    total_expenses: float
#    expenses: dict


class IMonthStatisticRead(MonthBase):
    days_statistics: Dict 
    total_expenses: float
    savings: float
    user_telegram_id: int

class IDaysLimitsUpdate(SQLModel):
    days: Dict[str, float]
