from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import async_scoped_session
from asyncio import current_task
from ..core.config import settings


class AsyncDatabase:
    def __init__(self, url, echo: bool = True):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def create_tables(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)


db = AsyncDatabase(
    url=settings.db_url,
    echo=settings.db_echo
)
