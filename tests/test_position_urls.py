from httpx import AsyncClient

from src.core.services.permissions import (is_administrator,
                                           is_administrator_or_staff,
                                           is_user_authenticated)

from .conftest import app

app.dependency_overrides[is_user_authenticated] = lambda: None
app.dependency_overrides[is_administrator] = lambda: None
app.dependency_overrides[is_administrator_or_staff] = lambda: None


async def test_read_positions(aclient: AsyncClient):
    response = await aclient.get('/positions/')
    assert response.status_code == 200
    assert response.json() == []


async def test_create_position(aclient: AsyncClient):
    response = await aclient.post('/positions/', json={'title': 'Уборщик'})
    assert response.status_code == 201
    assert response.json()['title'] == 'Уборщик'


async def test_read_position_by_id(aclient: AsyncClient):
    response = await aclient.get('/positions/1/')
    assert response.status_code == 200
    assert response.json()['title'] == 'Уборщик'


async def test_update_position(aclient: AsyncClient):
    response = await aclient.patch('/positions/1/', json={'title': 'Менеджер'})
    assert response.status_code == 200
    assert response.json()['title'] == 'Менеджер'


async def test_delete_position(aclient: AsyncClient):
    response = await aclient.delete('/positions/1/')
    assert response.status_code == 204
