from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings


class AsyncDatabase:
    def __init__(self, url: str, echo: bool = True):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    

db = AsyncDatabase(
    url=settings.get_db_url()
)
