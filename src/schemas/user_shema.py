from src.models.user import UserBase
from sqlmodel import SQLModel
from src.utils.time import Data, get_data_by_time_zone


class IUserCreate(UserBase):
    telegram_id: int
    password: str | None


class IUserRead(UserBase):
    telegram_id: int

class IUserDataRead(SQLModel):
    day: int
    month: int
    year: int
    time_zone: str
