from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
from src.models.base import Base


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
            await connection.run_sync(Base.create_all)


db = AsyncDatabase(
    url=settings.db_url,
    echo=settings.db_echo
)
