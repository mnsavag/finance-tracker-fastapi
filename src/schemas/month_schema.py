from typing import Dict
from sqlmodel import SQLModel
from src.models.month import MonthBase


class IMonthReadByUser(SQLModel):
    user_id: int

class ITransferSavings(SQLModel):
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
