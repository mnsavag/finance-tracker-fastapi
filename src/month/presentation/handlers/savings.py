@router.patch("/savings/transfer-to")
async def transer_to_savings(
    dayTransferSavings: IDayTransferSavings,
    month_service: MonthService = Depends(MonthService)
):
    
    month = await get_month_or_exception(
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
):
    
    month = await get_month_or_exception(
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
):
    """Send all month's money rest before specified day to savings"""
    month = await get_month_or_exception(
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
