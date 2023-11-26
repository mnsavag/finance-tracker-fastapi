from fastapi import APIRouter, Depends

from src.month.data.models import Month
from src.month.domain.services.expenses import ExpensesService
from src.month.domain.schemas.expenses import (
    ExpenseCreate
)
from src.month.dependencies import try_get_month


router = APIRouter()
# year-month-day

@router.post("/expense/{date}")
async def add_expense( 
    expense: ExpenseCreate,
    month: Month = Depends(try_get_month),
    month_service: ExpensesService = Depends(ExpensesService),
):
    month = await month_service.add_expense(month, day, expense)
    return month


@router.delete("/expense")
async def delete_expense(
    dayDeleteExpense: IDayExpenseDelete,
    month_service: MonthService = Depends(MonthService)
):
    
    month = await get_month_or_exception(
        user_id=dayDeleteExpense.user_id, 
        year=dayDeleteExpense.year, 
        month=dayDeleteExpense.month,
        day=dayDeleteExpense.day
    )
    
    try:
        month = await month_service.delete_expense(month, dayDeleteExpense.day, dayDeleteExpense)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return month
