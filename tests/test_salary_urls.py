from datetime import date, timedelta

from httpx import AsyncClient

from .conftest import dependency_overrides

before_date: date = date.today().strftime('%Y-%m-%d')
after_date: str = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
raise_date: str = (date.today() + timedelta(days=15)).strftime('%Y-%m-%d')
raise_date_next: str = (date.today() + timedelta(days=35)).strftime('%Y-%m-%d')


@dependency_overrides
async def test_read_salaries(aclient: AsyncClient):
    response = await aclient.get('/salaries/')
    assert response.status_code == 200
    assert response.json() == []


@dependency_overrides
async def test_read_salaries_with_params(aclient: AsyncClient):
    response = await aclient.get(
        '/salaries/',
        params={'after_date': after_date, 'before_date': before_date}
    )
    assert response.status_code == 200
    assert response.json() == []


@dependency_overrides
async def test_create_salary(aclient: AsyncClient):
    response = await aclient.post(
        '/salaries/',
        json={'amount': 1000.04, 'raise_date': raise_date}
    )
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'amount': 1000.04,
        'raise_date': raise_date,
        'employee': None
    }


@dependency_overrides
async def test_read_salaries_with_params_again(aclient: AsyncClient):
    response = await aclient.get(
        '/salaries/',
        params={'after_date': after_date, 'before_date': before_date}
    )
    assert response.status_code == 200
    assert response.json() == [{
        'id': 1,
        'amount': 1000.04,
        'raise_date': raise_date,
        'employee': None
    }]


@dependency_overrides
async def test_read_salary_by_id(aclient: AsyncClient):
    response = await aclient.get('/salaries/1/')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'amount': 1000.04,
        'raise_date': raise_date,
        'employee': None
    }


@dependency_overrides
async def test_update_salary(aclient: AsyncClient):
    response = await aclient.patch(
        '/salaries/1/', json={'amount': 1500.04, 'raise_date': raise_date_next}
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'amount': 1500.04,
        'raise_date': raise_date_next,
        'employee': None
    }


@dependency_overrides
async def test_delete_salary(aclient: AsyncClient):
    response = await aclient.delete('/salaries/1/')
    assert response.status_code == 204
