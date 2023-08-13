import asyncio
from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)

from src.core.services.authentication_service import AuthenticationService
from src.core.settings import settings
from src.data_base.models import Department, Position, Salary, User

DB_URL: str = settings.DB_DEV
if not settings.DEVELOPMENT:
    DB_URL: str = settings.get_postgresql_url

admin = User(
    first_name='Админ',
    last_name='Админыч',
    username='your',
    password=AuthenticationService.get_password_hash('salary2023'),
    date_of_birth=date(1990, 1, 21),
    status='admin',
    is_blocked=False,
    department=Department(
        title='ИТ-отдел'
    ),
    position=Position(
        title='Администратор'
    ),
    salary=Salary(
        amount=99999.99,
        raise_date=date(2024, 1, 1)
    )
)
staff = User(
    first_name='Иван',
    last_name='Иванов',
    username='cadr',
    password=AuthenticationService.get_password_hash('12345678'),
    date_of_birth=date(2000, 10, 21),
    status='staff',
    is_blocked=False,
    department=Department(
        title='Отдел кадров'
    ),
    position=Position(
        title='Кадровик'
    ),
    salary=Salary(
        amount=199999.99,
        raise_date=date(2025, 1, 1)
    )
)
employee_1 = User(
    first_name='Вася',
    last_name='Васечкин',
    username='vasya',
    password=AuthenticationService.get_password_hash('12345678'),
    date_of_birth=date(1995, 10, 8),
    status='employee',
    is_blocked=False,
    department=Department(
        title='Технологический отдел'
    ),
    position=Position(
        title='Технолог'
    ),
    salary=Salary(
        amount=59999.99,
        raise_date=date(2023, 8, 1)
    )
)
employee_2 = User(
    first_name='Сергей',
    last_name='Сергеев',
    username='serega',
    password=AuthenticationService.get_password_hash('12345678'),
    date_of_birth=date(1997, 11, 3),
    status='employee',
    is_blocked=False,
    department_id=3,
    position=Position(
        title='Главный технолог'
    ),
    salary=Salary(
        amount=79999.99,
        raise_date=date(2023, 11, 1)
    )
)
employee_3 = User(
    first_name='Татьяна',
    last_name='Петрова',
    username='tanya',
    password=AuthenticationService.get_password_hash('12345678'),
    date_of_birth=date(1997, 11, 7),
    status='employee',
    is_blocked=False,
    department=Department(
        title='Бухгалтерия'
    ),
    position=Position(
        title='Бухгалтер'
    ),
    salary=Salary(
        amount=299999.99,
        raise_date=date(2023, 7, 1)
    )
)


async def create_fake_data(engine: AsyncEngine) -> None:
    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all([admin, staff, employee_1, employee_2, employee_3])


if __name__ == '__main__':
    engine = create_async_engine(
        url=DB_URL,
        echo=True
    )
    try:
        asyncio.run(create_fake_data(engine))
    except IntegrityError:
        raise SystemExit('База уже наполнена данными!')
