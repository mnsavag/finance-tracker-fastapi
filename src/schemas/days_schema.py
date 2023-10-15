from sqlmodel import SQLModel


class IDataMonthYear(SQLModel):
    year: int
    month: int

class IData(SQLModel):
    year: int
    month: int
    day: int


class ISetLimit(IData):
    user_id: int
    limit: float


class IExpenseCreate(IData):
    user_id: int
    name: str
    cost: int

class IExpenseDelete(IData):
    user_id: int
    name: str
