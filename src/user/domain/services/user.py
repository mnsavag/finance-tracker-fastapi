from src.user.data.models import User
from src.user.domain.schemas import UserCreate
from src.user.data.repositories.user import UserRepository
from src.user.exceptions import UserExistException
from src.sql_alchemy_repository  import IRepositoryBase


class UserService:
    user_repo: IRepositoryBase = UserRepository()

    async def add_user(self, user: UserCreate) -> User:
        await self.try_validate_user(user.telegram_id, user.mail)
        return await self.user_repo.create(user)
        
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.user_repo.get_by_telegram_id(telegram_id)

    async def try_validate_user(self, telegram_id: int, mail: str) -> bool:
        user_by_id = await self.user_repo.get_by_telegram_id(telegram_id)
        user_by_mail = await self.user_repo.get_by_mail(mail)
        if user_by_id:
            raise UserExistException(id=telegram_id)
        if user_by_mail:
            raise UserExistException(mail=mail)
        return True
