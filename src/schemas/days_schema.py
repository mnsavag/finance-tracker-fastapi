from sqlmodel import SQLModel


class ISetLimit(SQLModel):
    user_id: int
    time_zone: str
    limit: float


class IExpenseCreate(SQLModel):
    user_id: int
    name: str
    cost: int

class IExpenseDelete(SQLModel):
    user_id: int
    name: str
