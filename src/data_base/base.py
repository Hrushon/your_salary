from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..core.settings import settings  # noqa

# DB_URL: str = settings.get_postgresql_url
DB_URL: str = 'sqlite+aiosqlite:///./db.sqlite3'

echo: bool = True if settings.DEBUG else False

# engine = create_async_engine(
#   url=DB_URL,
#   echo=echo,
#   pool_pre_ping=True???? узнать для чего это
# )
engine = create_async_engine(
    url=DB_URL,
    echo=echo,
    connect_args={"check_same_thread": False},
)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
