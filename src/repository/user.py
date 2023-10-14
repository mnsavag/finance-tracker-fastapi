from src.db.db import db
from src.schemas.user_shema import IUserCreate
from src.models.user import User
from src.core.security import get_password_hash
from sqlalchemy.sql import select
from src.models.month import Month
from src.repository.repositoryBase import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_by_mail(self, mail: str) -> User | None:
        async with db.session_factory() as session:
            stmt = select(User).where(User.mail == mail)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
    
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        async with db.session_factory() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
