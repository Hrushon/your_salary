from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..core.settings import settings  # noqa

echo: bool = True if settings.DEBUG else False

if not settings.DEVELOPMENT:
    db_url: str = settings.get_postgresql_url
    engine = create_async_engine(
        url=db_url,
        echo=echo,
        pool_pre_ping=True
    )
else:
    db_url: str = settings.DB_DEV
    engine = create_async_engine(
        url=db_url,
        echo=echo,
        connect_args={"check_same_thread": False},
    )

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
