from datetime import datetime
from typing import Optional
from pytz import timezone
from sqlmodel import SQLModel


class Data(SQLModel):
    day: Optional[int]
    month: Optional[int]
    year: Optional[int]


async def get_data_by_time_zone(time_zone):
    time = timezone(time_zone)
    sa_time = datetime.now(time)
    year, month, day = sa_time.strftime('%Y-%m-%d').split('-')
    return Data(day=day, month=month, year=year)
