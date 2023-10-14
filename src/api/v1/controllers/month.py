from typing import Annotated, List
from fastapi import APIRouter, Depends, status, HTTPException

from src.models.month import MonthBase, Month

from src.schemas.response_shema import create_response

from src.repository.user import UserRepository
from src.deps.services import get_user_service, get_month_service
from src.services.month import MonthService

from src.repository.user import UserRepository
from src.models.user import User
from src.services.user import UserService

from src.utils.exceptions.user import UserNotFoundException
from src.utils.exceptions.month import MonthNotFoundException
from src.utils.exceptions.common import IdNotFoundException

from src.utils.time import get_data_by_time_zone, Data

from src.schemas.days_schema import ISetLimit, IExpenseCreate, IExpenseDelete
from src.schemas.month_schema import IMonthReadByUser, ITransferSavings

from src.deps.user import get_user
from src.models.month import Month

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


@router.get("/current")
async def get_current_month(
    obj_in: MonthBase,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    data: Data = await get_data_by_time_zone(obj_in.time_zone)
    month = await month_service.get_current_month(obj_in.user_telegram_id, data)
    if not month:
        raise MonthNotFoundException(obj_in.user_telegram_id)
    return month


@router.get("/{year}/{month}")
async def get_month(
    monthRead: IMonthReadByUser,
    year: int,
    month: int,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_data(monthRead.user_id, Data(year=year, month=month))
    if not month:
        raise MonthNotFoundException(monthRead.user_id)
    return month


@router.patch("/limits")
async def set_limits(
    obj_in: ISetLimit,
    month_service: MonthService = Depends(MonthService)
) -> dict:
    
    data: Data = await get_data_by_time_zone(obj_in.time_zone)
    month = await month_service.get_current_month(obj_in.user_id, data)
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    daily_stats = await month_service.set_limits_after_day(month, data.day, obj_in.limit)
    return daily_stats


@router.post("/{year}/{month}/{day}/expense")
async def add_expense( 
    expense: IExpenseCreate,

    year: int,
    month: int,
    day: int,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_data(expense.user_id, Data(year=year, month=month, day=day))
    if not month:
        raise MonthNotFoundException(expense.user_id)
    
    month = await month_service.add_expense(month, day, expense)
    return month


@router.delete("/{year}/{month}/{day}/expense")
async def delete_expense(
    expense: IExpenseDelete,

    year: int,
    month: int,
    day: int,
    month_service: MonthService = Depends(MonthService)

) -> Month:
    
    month = await month_service.get_by_user_id_and_data(expense.user_id, Data(year=year, month=month, day=day))
    if not month:
        raise MonthNotFoundException(expense.user_id)
    
    if expense.name not in month.days_statistics[str(day)]["expenses"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{expense.name} not found",
        )
    
    month = await month_service.delete_expense(month, day, expense)
    return month


@router.patch("/{year}/{month}/{day}/to-savings")
async def transer_to_savings(
    obj_in: ITransferSavings,

    year: int,
    month: int,
    day: int,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_data(obj_in.user_id, Data(year=year, month=month, day=day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    month = await month_service.transfer_to_savings(month, day, obj_in.amount)
    return month

@router.patch("/{year}/{month}/{day}/from-savings")
async def transer_to_savings(
    obj_in: ITransferSavings,

    year: int,
    month: int,
    day: int,
    month_service: MonthService = Depends(MonthService)
) -> Month:
    
    month = await month_service.get_by_user_id_and_data(obj_in.user_id, Data(year=year, month=month, day=day))
    if not month:
        raise MonthNotFoundException(obj_in.user_id)
    
    month = await month_service.transfer_from_savings(month, day, obj_in.amount)
    return month
