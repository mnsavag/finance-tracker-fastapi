from typing import Any, Dict
from pydantic import BaseModel, Json
from src.schemas.date_scheme import DateMonthYear


class IMonthDefined(DateMonthYear):
    telegram_user_id: int

class IMonthCreate(DateMonthYear):
    telegram_user_id: int
    days_statistics: dict 

class IMonth(DateMonthYear):
    id: int
    user_telegram_id: int
    days_statistics: dict = {}
    total_expenses: float
    savings: float
