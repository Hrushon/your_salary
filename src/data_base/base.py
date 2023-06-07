from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..core.settings import settings  # noqa

echo: bool = True if settings.DEBUG else False

DB_URL: str = settings.DB_DEV
engine = create_async_engine(
    url=DB_URL,
    echo=echo,
    connect_args={"check_same_thread": False},
)

if not settings.DEVELOPMENT:
    DB_URL: str = settings.get_postgresql_url
    engine = create_async_engine(
        url=DB_URL,
        echo=echo,
        pool_pre_ping=True
    )

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
