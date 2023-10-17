from typing import Dict
from pydantic import BaseModel
from src.schemas.date_scheme import DateFull

    
class IDaysLimitsUpdate(BaseModel):
    days: Dict[str, float]

class IDayRead(DateFull):
    user_id: int

class IDayReadLimit(IDayRead):
    limit: float

class IDayExpenseCreate(IDayRead):
    name: str
    cost: int

class IDayExpenseDelete(IDayRead):
    name: str

class IDayTransferSavings(IDayRead):
    amount: int
