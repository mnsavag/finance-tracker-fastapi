from pydantic import BaseModel
from typing import Optional


class Date(BaseModel):
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]

class DateFull(BaseModel):
    year: int
    month: int
    day: int

class DateMonthYear(BaseModel):
    year: int
    month: int
