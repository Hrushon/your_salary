from httpx import AsyncClient

from src.core.services.permissions import (is_administrator,
                                           is_administrator_or_staff,
                                           is_user_authenticated)

from .conftest import app

app.dependency_overrides[is_user_authenticated] = lambda: None
app.dependency_overrides[is_administrator] = lambda: None
app.dependency_overrides[is_administrator_or_staff] = lambda: None


async def test_read_departments(aclient: AsyncClient):
    response = await aclient.get('/departments/')
    assert response.status_code == 200
    assert response.json() == []


async def test_create_department(aclient: AsyncClient):
    response = await aclient.post(
        '/departments/', json={'title': 'Текущий ремонт'}
    )
    assert response.status_code == 201
    assert response.json()['title'] == 'Текущий ремонт'


async def test_read_department_by_id(aclient: AsyncClient):
    response = await aclient.get('/departments/1/')
    assert response.status_code == 200
    assert response.json()['title'] == 'Текущий ремонт'


async def test_update_department(aclient: AsyncClient):
    response = await aclient.patch(
        '/departments/1/', json={'title': 'Экономический отдел'}
    )
    assert response.status_code == 200
    assert response.json()['title'] == 'Экономический отдел'


async def test_delete_department(aclient: AsyncClient):
    response = await aclient.delete('/departments/1/')
    assert response.status_code == 204
