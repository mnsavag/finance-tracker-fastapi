from src.month.domain.schemas.date import DateMonthYear


class MonthDefined(DateMonthYear):
    telegram_user_id: int

class MonthCreate(DateMonthYear):
    telegram_user_id: int
    days_statistics: dict 

class Month(DateMonthYear):
    id: int
    user_telegram_id: int
    days_statistics: dict
    total_expenses: float
    savings: float
