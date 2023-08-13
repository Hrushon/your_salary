import asyncio
from datetime import date, timedelta
from functools import wraps
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.api_main import create_application
from src.core.services.authentication_service import AuthenticationService
from src.core.services.permissions import (is_administrator,
                                           is_administrator_or_staff,
                                           is_user_authenticated)
from src.core.settings import settings
from src.data_base.base import get_session
from src.data_base.models import Base, Department, Position, Salary, User

database_url_test: str = settings.get_test_base_url
if settings.DEVELOPMENT:
    database_url_test: str = settings.DB_DEV_TEST


raise_date: date = date.today() + timedelta(days=15)

app: FastAPI = create_application()
metadata: MetaData = Base.metadata
base_url: str = 'http://test/api/v1'

engine_test = create_async_engine(database_url_test, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


def dependency_overrides(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        app.dependency_overrides[is_user_authenticated] = lambda: None
        app.dependency_overrides[is_administrator] = lambda: None
        app.dependency_overrides[is_administrator_or_staff] = lambda: None
        await func(*args, **kwargs)
        app.dependency_overrides[is_user_authenticated] = {}
        app.dependency_overrides[is_administrator] = {}
        app.dependency_overrides[is_administrator_or_staff] = {}
    return wrap


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope='module')
async def create_secondary_data():
    department = Department(title='Тестовый отдел')
    position = Position(title='Тестовая должность')
    salary = Salary(
        amount=99999.99,
        raise_date=raise_date
    )
    async with async_session_maker() as session:
        session.add_all([department, position, salary])
        await session.commit()


@pytest.fixture(scope='module')
async def create_auth_needs_data():
    admin = User(
        first_name='Админ',
        last_name='Админыч',
        username='admin',
        password=AuthenticationService.get_password_hash('12345678'),
        date_of_birth=date(1990, 1, 21),
        status='admin',
        is_blocked=False
    )
    staff = User(
        first_name='Иван',
        last_name='Иванов',
        username='staff',
        password=AuthenticationService.get_password_hash('12345678'),
        date_of_birth=date(2000, 10, 21),
        status='staff',
        is_blocked=False
    )
    employee = User(
        first_name='Вася',
        last_name='Васечкин',
        username='employee',
        password=AuthenticationService.get_password_hash('12345678'),
        date_of_birth=date(1995, 10, 8),
        status='employee',
        is_blocked=False
    )
    async with async_session_maker() as session:
        session.add_all([admin, staff, employee])
        await session.commit()


@pytest.fixture(scope='module')
async def get_tokens(
    aclient: AsyncClient, create_auth_needs_data: None  # noqa
) -> dict[str, str]:
    result: dict = dict()
    token = await aclient.post('/employees/login/', json={
        'username': 'admin',
        'password': '12345678'
    })
    result['admin'] = token.json()['access_token']
    token = await aclient.post('/employees/login/', json={
        'username': 'staff',
        'password': '12345678'
    })
    result['staff'] = token.json()['access_token']
    token = await aclient.post('/employees/login/', json={
        'username': 'employee',
        'password': '12345678'
    })
    result['employee'] = token.json()['access_token']
    return result


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


@pytest.fixture(scope='session')
async def aclient() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        yield ac
