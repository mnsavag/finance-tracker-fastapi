@router.patch("/limits")
async def set_limits(
    dayReadLimit: IDayReadLimit,
    month_service: MonthService = Depends(MonthService)
):
    
    month = await get_month_or_exception(
        user_id=dayReadLimit.user_id, 
        year=dayReadLimit.year, 
        month=dayReadLimit.month,
        day=dayReadLimit.day
    )
    
    try:
        month = await month_service.set_limits_after_day(month, dayReadLimit.day, dayReadLimit.limit)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return month


@router.patch("/limit")
async def set_limit(
    dayReadLimit: IDayReadLimit,
    month_service: MonthService = Depends(MonthService)
):
    
    month = await get_month_or_exception(
        user_id=dayReadLimit.user_id, 
        year=dayReadLimit.year, 
        month=dayReadLimit.month,
        day=dayReadLimit.day
    )
    
    try:
        month = await month_service.set_day_limit(month, dayReadLimit.day, dayReadLimit.limit)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return month


@router.patch("/{month_id}/limits/transfer")
async def transfer_limits(
    limits: IDaysLimitsUpdate,
    month_id: int,
    month_service: MonthService = Depends(MonthService)
) -> dict:
    """Compares request and db limits and if there are no data integrity violations, then updates"""
    month = await month_service.get_by_id(month_id)
    if not month:
        raise IdNotFoundException(Month, month_id)

    try:
        await month_service.transfer_limits(month, limits.days)
    except Exception as e:
        raise UnprocessableEntityException(str(e))
    return create_response(detail="limits updated")
