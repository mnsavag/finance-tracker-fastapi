from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    telegram_id: int
    password: str
    email: EmailStr

class UserOut(BaseModel):
    telegram_id: int
    email: EmailStr
    created_at: datetime
