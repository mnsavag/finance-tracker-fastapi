from pydantic import BaseModel

from src.month.domain.schemas.day import DayRead


class ExpenseCreate(BaseModel):
    name: str
    cost: int

class DayExpenseDelete(DayRead):
    name: str

class DayTransferSavings(DayRead):
    amount: int
