from sqlmodel import SQLModel
from typing import Dict
from src.schemas.date_scheme import DateFull

    
class IDayRead(DateFull):
    user_id: int


class IDaysLimitsUpdate(SQLModel):
    days: Dict[str, float]

class IDayReadLimit(IDayRead):
    limit: float

class IDayExpenseCreate(IDayRead):
    name: str
    cost: int

class IDayExpenseDelete(IDayRead):
    name: str

class IDayTransferSavings(IDayRead):
    amount: int
