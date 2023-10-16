from sqlmodel import SQLModel
from src.schemas.date_scheme import DateFull, DateMonthYear

class ISetLimit(DateFull):
    user_id: int
    limit: float


class IExpenseCreate(DateFull):
    user_id: int
    name: str
    cost: int

class IExpenseDelete(DateFull):
    user_id: int
    name: str
