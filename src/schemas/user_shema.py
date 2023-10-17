from pydantic import BaseModel, EmailStr

class IUserCreate(BaseModel):
    telegram_id: int
    password: str | None
    mail: EmailStr
