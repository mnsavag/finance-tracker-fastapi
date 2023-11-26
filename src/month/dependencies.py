from fastapi import HTTPException, status

from src.month.domain.schemas.date import Date
from src.month.domain.services.month import MonthService
from src.month.exceptions import InvalidDateFormatException


async def try_get_month(
    user_id: int, 
    date: str
):
    date = Date(year=year, month=month, day=day)
    month = await MonthService().get_month(user_id, date)
    if not month:
        raise NotFoundException(
            detail=f"Unable to find month {day}:{month}:{year} of the user with id {user_id}."
        )
    return month


#year-month-day
async def try_get_date(date: str) -> Date:
    data = date.split("-")
    if len(data) != 3:
        raise InvalidDateFormatException()
    for item in data:
        if not item.isdigit():
            raise InvalidDateFormatException()
    return Date(year=data[0], month=data[1], day=data[2])
