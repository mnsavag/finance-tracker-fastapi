from datetime import datetime
from pytz import timezone
from src.schemas.date_scheme import Date


async def get_date_by_time_zone(time_zone):
    time = timezone(time_zone)
    sa_time = datetime.now(time)
    year, month, day = sa_time.strftime('%Y-%m-%d').split('-')
    return Date(day=day, month=month, year=year)
