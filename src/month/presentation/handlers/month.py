router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_month(
    month_create: IMonthDefined,
    user_service: UserService = Depends(UserService),
    month_service: MonthService = Depends(MonthService)
) -> dict:
    
    user = await user_service.get_by_telegram_id(month_create.telegram_user_id)
    if not user:
        raise UserNotFoundException(month_create.telegram_user_id)
    
    await month_service.add_month_to_user(month_create, user)
    return create_response(detail="Month created")


@router.get("")
async def get_month(definedMonth: IMonthDefined): 
    month = await get_month_or_exception(
        user_id=definedMonth.telegram_user_id, 
        year=definedMonth.year, 
        month=definedMonth.month
    )
    return month
