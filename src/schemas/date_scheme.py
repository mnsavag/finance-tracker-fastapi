from sqlmodel import SQLModel
from typing import Optional


class Date(SQLModel):
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]

class DateFull(SQLModel):
    year: int
    month: int
    day: int

class DateMonthYear(SQLModel):
    year: int
    month: int
