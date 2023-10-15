from typing import Dict
from sqlmodel import SQLModel
from src.models.month import MonthBase


class IDataMonthYear(SQLModel):
    year: int
    month: int

class IData(SQLModel):
    year: int
    month: int
    day: int


class ISpecificMonth(IDataMonthYear):
    user_id: int


class ITransferSavings(IData):
    user_id: int
    amount: int
    
class IDayStats(SQLModel):
    limit: float
    money_rest: float
    total_expenses: float
    expenses: dict

class IMonthStatisticRead(MonthBase):
    days_statistics: Dict 
    total_expenses: float
    savings: float
    user_telegram_id: int
