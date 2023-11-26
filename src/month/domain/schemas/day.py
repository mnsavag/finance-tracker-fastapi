from typing import Dict
from pydantic import BaseModel

from src.month.domain.schemas.date import DateFull

    
class DaysLimitsUpdate(BaseModel):
    days: Dict[str, float]

class DayRead(DateFull):
    user_id: int

class DayReadLimit(DayRead):
    limit: float
