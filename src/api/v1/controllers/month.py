from fastapi import APIRouter, Depends, status

from src.models.month import MonthBase, Month

from src.services.user import UserService
from src.services.month import MonthService

from src.utils.exceptions import (
        UserNotFoundException, 
        IdNotFoundException, 
        UnprocessableEntityException
    )

from src.schemas.response_shema import create_response
from src.schemas.month_schema import IMonthRead
from src.schemas.days_schema import (
        IDayRead, 
        IDayReadLimit, 
        IDayExpenseCreate, IDayExpenseDelete, 
        IDayTransferSavings, 
        IDaysLimitsUpdate
    )
from src.utils.month_checks import get_month_or_exception


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_month(
    obj_in: MonthBase,
    user_service: UserService = Depends(UserService),
    month_service: MonthService = Depends(MonthService)
):
    
    user = await user_service.get_by_telegram_id(obj_in.user_telegram_id)
    if not user:
        raise UserNotFoundException(obj_in.user_telegram_id)
    
    month: Month = await Month.get_init_month(obj_in.time_zone)
    await month_service.add_month_to_user(month, user)
    return create_response(detail="Month created")


@router.get("")
async def get_month(
    monthRead: IMonthRead,
) -> Month:
    
    month: Month = await get_month_or_exception(
        user_id=monthRead.user_id, 
        year=monthRead.year, 
        month=monthRead.month
    )
    return month


@router.patch("/limits")
async def set_limits(
    dayReadLimit: IDayReadLimit,
    month_service: MonthService = Depends(MonthService)
) -> dict:
    
    month: Month = await get_month_or_exception(
        user_id=dayReadLimit.user_id, 
        year=dayReadLimit.year, 
        month=dayReadLimit.month,
        day=dayReadLimit.day
    )
    
    try:
        daily_stats = await month_service.set_limits_after_day(month, dayReadLimit.day, dayReadLimit.limit)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return daily_stats


@router.patch("/limit")
async def set_limit(
    dayReadLimit: IDayReadLimit,
    month_service: MonthService = Depends(MonthService)
) -> dict:
    
    month: Month = await get_month_or_exception(
        user_id=dayReadLimit.user_id, 
        year=dayReadLimit.year, 
        month=dayReadLimit.month,
        day=dayReadLimit.day
    )
    
    try:
        daily_stats = await month_service.set_day_limit(month, dayReadLimit.day, dayReadLimit.limit)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return daily_stats


@router.post("/expense")
async def add_expense( 
    dayCreateExpense: IDayExpenseCreate,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month: Month = await get_month_or_exception(
        user_id=dayCreateExpense.user_id, 
        year=dayCreateExpense.year, 
        month=dayCreateExpense.month,
        day=dayCreateExpense.day
    )
    month = await month_service.add_expense(month, dayCreateExpense.day, dayCreateExpense)
    return month


@router.delete("/expense")
async def delete_expense(
    dayDeleteExpense: IDayExpenseDelete,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month: Month = await get_month_or_exception(
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


@router.patch("/savings/transfer-to")
async def transer_to_savings(
    dayTransferSavings: IDayTransferSavings,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month: Month = await get_month_or_exception(
        user_id=dayTransferSavings.user_id, 
        year=dayTransferSavings.year, 
        month=dayTransferSavings.month,
        day=dayTransferSavings.day
    )
    
    try:
        month = await month_service.transfer_to_savings(month, dayTransferSavings.day, dayTransferSavings.amount)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return month


@router.patch("/savings/transfer-from")
async def transer_from_savings(
    dayTransferSavings: IDayTransferSavings,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month: Month = await get_month_or_exception(
        user_id=dayTransferSavings.user_id, 
        year=dayTransferSavings.year, 
        month=dayTransferSavings.month,
        day=dayTransferSavings.day
    )
     
    try:
        month = await month_service.transfer_from_savings(month, dayTransferSavings.day, dayTransferSavings.amount)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return month


@router.patch("/rest/send-to-savings")
async def rest_to_savings(
    dayRead: IDayRead,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    """Send all month's money rest before specified day to savings"""
    month: Month = await get_month_or_exception(
        user_id=dayRead.user_id, 
        year=dayRead.year, 
        month=dayRead.month,
        day=dayRead.day
    )

    try:
        month = await month_service.rest_to_savings(month, dayRead.day)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return month


@router.patch("/rest/send-in-a-day")
async def rest_in_a_day(
    dayRead: IDayRead,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    """Send all month's money rest before specified day in a day"""
    month: Month = await get_month_or_exception(
        user_id=dayRead.user_id, 
        year=dayRead.year, 
        month=dayRead.month,
        day=dayRead.day
    )

    try:
        month = await month_service.rest_in_a_day(month, dayRead.day)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return month


@router.patch("/{month_id}/limits/transfer")
async def transfer_limits(
    limits: IDaysLimitsUpdate,
    month_id: int,
    month_service: MonthService = Depends(MonthService)
):
    """Compares request and db limits and if there are no data integrity violations, then updates"""
    month = await month_service.get_by_id(month_id)
    if not month:
        raise IdNotFoundException(Month, month_id)

    try:
        await month_service.transfer_limits(month, limits.days)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return create_response(detail="limits updated")
