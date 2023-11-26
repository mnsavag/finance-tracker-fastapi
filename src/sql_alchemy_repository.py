from abc import ABC, abstractmethod
from sqlalchemy.sql import select
from typing import List, TypeVar

from src.database import db


ModelType = TypeVar('ModelType')


class IRepositoryBase(ABC):
    @abstractmethod
    async def create():
        raise NotImplementedError
    

class SQLAlchemyRepository(IRepositoryBase):
    model = None

    async def get_by_id(self, id: int) -> ModelType | None:
        async with db.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            response = await session.execute(stmt)
            return response.scalar_one_or_none()

    async def update(self, obj) -> ModelType | None:
       async with db.session_factory() as session:
           session.add(obj)
           await session.commit()
           await session.refresh(obj)
           return obj
