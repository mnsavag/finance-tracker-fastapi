from fastapi import APIRouter, Depends, status

from src.models.month import Month
from src.services.user import UserService
from src.services.month import MonthService

from src.utils.exceptions import (
        UserNotFoundException, 
        IdNotFoundException, 
        UnprocessableEntityException
    )

from src.schemas.response_shema import create_response
from src.schemas.month_schema import IMonthDefined
from src.schemas.days_schema import (
        IDayRead, 
        IDayReadLimit, 
        IDayExpenseCreate, IDayExpenseDelete, 
        IDayTransferSavings, 
        IDaysLimitsUpdate
    )
from src.utils.month_checks import get_month_or_exception



@router.patch("/rest/send-in-a-day")
async def rest_in_a_day(
    dayRead: IDayRead,
    month_service: MonthService = Depends(MonthService)
):
    """Send all month's money rest before specified day in a day"""
    month = await get_month_or_exception(
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
