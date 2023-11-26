from src.services.user import UserService
from src.models.user import User
from src.utils.exceptions.user import UserNotFoundException


async def is_(user_telegram_id: int) -> User:
    user = await UserService.get_by_telegram_id(user_telegram_id)
    if not user:
        raise UserNotFoundException(User, id=user_telegram_id)
    return user
