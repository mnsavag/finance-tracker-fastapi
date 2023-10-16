from fastapi import APIRouter, Depends, status, HTTPException

from src.models.month import MonthBase, Month

from src.services.month import MonthService
from src.services.user import UserService

from src.utils.exceptions.user import UserNotFoundException
from src.utils.exceptions.month import MonthNotFoundException
from src.utils.exceptions.common import IdNotFoundException

from src.schemas.date_scheme import Date
from src.schemas.days_schema import ISetLimit, IExpenseCreate, IExpenseDelete
from src.schemas.month_schema import ISpecificMonth, ISpecificDate, ITransferSavings, IDaysLimitsUpdate
from src.schemas.response_shema import create_response


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
    specificMonth: ISpecificMonth,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_date(specificMonth.user_id, Date(year=specificMonth.year, month=specificMonth.month))
    if not month:
        raise MonthNotFoundException(specificMonth.user_id)
    return month


@router.patch("/limits")
async def set_limits(
    obj_in: ISetLimit,
    month_service: MonthService = Depends(MonthService)
) -> dict:
    
    date: Date = Date(year=obj_in.year, month=obj_in.month, day=obj_in.day)
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, date)
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    daily_stats = await month_service.set_limits_after_day(month, obj_in.day, obj_in.limit)
    return daily_stats


@router.patch("/limit")
async def set_limit(
    obj_in: ISetLimit,
    month_service: MonthService = Depends(MonthService)
) -> dict:
    
    date: Date = Date(year=obj_in.year, month=obj_in.month, day=obj_in.day)
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, date)
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    daily_stats = await month_service.set_day_limit(month, obj_in.day, obj_in.limit)
    return daily_stats


@router.post("/expense")
async def add_expense( 
    obj_in: IExpenseCreate,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, Date(year=obj_in.year, month=obj_in.month, day=obj_in.day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    month = await month_service.add_expense(month, obj_in.day, obj_in)
    return month


@router.delete("/expense")
async def delete_expense(
    obj_in: IExpenseDelete,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, Date(year=obj_in.year, month=obj_in.month, day=obj_in.day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    if obj_in.name not in month.days_statistics[str(obj_in.day)]["expenses"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{obj_in.name} not found",
        )
    
    month = await month_service.delete_expense(month, obj_in.day, obj_in)
    return month


@router.patch("/savings/transfer-to")
async def transer_to_savings(
    obj_in: ITransferSavings,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, Date(year=obj_in.year, month=obj_in.month, day=obj_in.day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    month = await month_service.transfer_to_savings(month, obj_in.day, obj_in.amount)
    return month


@router.patch("/savings/transfer-from")
async def transer_from_savings(
    obj_in: ITransferSavings,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, Date(year=obj_in.year, month=obj_in.month, day=obj_in.day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    month = await month_service.transfer_from_savings(month, obj_in.day, obj_in.amount)
    return month


@router.patch("/rest/send-to-savings")
async def rest_to_savings(
    obj_in: ISpecificDate,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    """Send all month's money rest before specified day to savings"""
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, Date(year=obj_in.year, month=obj_in.month, day=obj_in.day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    month = await month_service.rest_to_savings(month, obj_in.day)
    return month


@router.patch("/rest/send-in-a-day")
async def rest_to_savings(
    obj_in: ISpecificDate,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    """Send all month's money rest before specified day in a day"""
    month = await month_service.get_by_user_id_and_date(obj_in.user_id, Date(year=obj_in.year, month=obj_in.month, day=obj_in.day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    month = await month_service.rest_in_a_day(month, obj_in.day)
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

    await month_service.transfer_limits(month, limits.days)
    return create_response(detail="limits updated")
