from src.models.user import User
from src.schemas.user_shema import IUserCreate
from src.repository.user import UserRepository
from src.repository.repositoryBase  import IRepositoryBase
from src.utils.exceptions.user import UserExistException


class UserService:
    user_repo: IRepositoryBase = UserRepository()

    async def add_user(self, user: IUserCreate) -> None:
        await self.is_unique_user(user.telegram_id, user.mail)
        await self.user_repo.create(dict(user))

        
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.user_repo.get_by_telegram_id(telegram_id)

    async def is_unique_user(self, telegram_id: int, mail: str) -> bool:
        user_by_id = await self.user_repo.get_by_telegram_id(telegram_id)
        user_by_mail = await self.user_repo.get_by_mail(mail)
        if user_by_id:
            raise UserExistException(id=telegram_id)
        if user_by_mail:
            raise UserExistException(mail=mail)
        return True
