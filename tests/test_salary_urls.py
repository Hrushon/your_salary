from datetime import date, timedelta

from httpx import AsyncClient

from src.core.services.permissions import (is_administrator,
                                           is_administrator_or_staff,
                                           is_user_authenticated)

from .conftest import app

app.dependency_overrides[is_user_authenticated] = lambda: None
app.dependency_overrides[is_administrator] = lambda: None
app.dependency_overrides[is_administrator_or_staff] = lambda: None

before_date: date = date.today().strftime('%Y-%m-%d')
after_date: str = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
raise_date: str = (date.today() + timedelta(days=15)).strftime('%Y-%m-%d')


async def test_read_salaries(aclient: AsyncClient):
    response = await aclient.get('/salaries/')
    assert response.status_code == 200
    assert response.json() == []


async def test_read_salaries_with_params(aclient: AsyncClient):
    response = await aclient.get(
        '/salaries/',
        params={'after_date': after_date, 'before_date': before_date}
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_create_salary(aclient: AsyncClient):
    response = await aclient.post(
        '/salaries/',
        json={'amount': 1000.04, 'raise_date': raise_date}
    )
    assert response.status_code == 201
    data = response.json()
    assert data['amount'] == 1000.04
    assert data['raise_date'] == raise_date


async def test_read_salaries_with_params_again(aclient: AsyncClient):
    response = await aclient.get(
        '/salaries/',
        params={'after_date': after_date, 'before_date': before_date}
    )
    assert response.status_code == 200
    data = response.json()[0]
    assert data['amount'] == 1000.04
    assert data['raise_date'] == raise_date


async def test_read_salary_by_id(aclient: AsyncClient):
    response = await aclient.get('/salaries/1/')
    assert response.status_code == 200
    data = response.json()
    assert data['amount'] == 1000.04
    assert data['raise_date'] == raise_date


async def test_update_salary(aclient: AsyncClient):
    response = await aclient.patch(
        '/salaries/1/', json={'amount': 1500.04}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['amount'] == 1500.04
    assert data['raise_date'] == raise_date


async def test_delete_salary(aclient: AsyncClient):
    response = await aclient.delete('/salaries/1/')
    assert response.status_code == 204
