from src.schemas.month_schema import IMonth
from src.services.month import MonthService
from src.utils.exceptions.month import MonthNotFoundException
from src.schemas.date_scheme import Date


async def get_month_or_exception(
        user_id: int, 
        year: int = None, 
        month: int = None, 
        day: int = None
    ):
    date = Date(year=year, month=month, day=day)
    month = await MonthService().get_month(user_id, date)
    if not month:
        raise MonthNotFoundException(user_id)
    return month
