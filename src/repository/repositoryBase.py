from abc import ABC, abstractmethod
from src.db.db import db
from sqlalchemy.sql import select


class IRepositoryBase(ABC):
    @abstractmethod
    async def create():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(IRepositoryBase):
    model = None

    async def get(self, id):
        async with db.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            response = await session.execute(stmt)
            return response.scalar_one_or_none()

    async def create(self, data: dict) -> None:
        async with db.session_factory() as session:
            session.add(self.model(**data))
            await session.commit()

    async def update(self, obj): # указать что возвращает
       async with db.session_factory() as session:
           session.add(obj)
           await session.commit()
           await session.refresh(obj)
           return obj
    
    async def find_all():
        raise NotImplementedError
