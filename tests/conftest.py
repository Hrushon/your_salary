import asyncio
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.api_main import create_application
from src.core.settings import settings
from src.data_base.base import get_session
from src.data_base.models import Base

DATABASE_URL_TEST: str = settings.get_test_base_url

app: FastAPI = create_application()
metadata: MetaData = Base.metadata
base_url: str = 'http://test/api/v1'

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope='module')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def aclient() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        yield ac
