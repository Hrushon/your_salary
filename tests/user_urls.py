from httpx import AsyncClient

from src.core.services.permissions import (is_administrator,
                                           is_administrator_or_staff,
                                           is_user_authenticated)

from .conftest import app

app.dependency_overrides[is_user_authenticated] = lambda: None
app.dependency_overrides[is_administrator] = lambda: None
app.dependency_overrides[is_administrator_or_staff] = lambda: None


async def test_hello():
    response = await test_asclient.get('/hello_api')
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_login_user():
    response = await test_asclient.post('/users/', json={})
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_read_users():
    response = await test_asclient.get('/users/', headers={})
    assert response.status_code == 200
    assert response.json() == [{'API': 'HELLO, HUMAN'}]


async def test_create_user():
    response = await test_asclient.post('/users/', json={})
    assert response.status_code == 201
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_read_self_user():
    response = await test_asclient.get('/users/me/', headers={})
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_update_self_user():
    response = await test_asclient.patch('/users/me/', headers={}, json=[])
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_read_user_by_id():
    response = await test_asclient.get('/users/{id}/', id=1, headers={})
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_update_user():
    response = await test_asclient.patch('/users/{id}/', id=1, headers=[], json=[])
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_update_status_user():
    response = await test_asclient.patch('/users/{id}/', id=1, headers={}, json={})
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_block_user_by_id():
    response = await test_asclient.get('/users/{id}/block/', id=1, headers={})
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_unblock_user_by_id():
    response = await test_asclient.get('/users/{id}/unblock/', id=1, headers=[])
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_update_password_user():
    response = await test_asclient.patch('/users/{id}/password_reset/', id=1, headers=[], json=[])
    assert response.status_code == 200
    assert response.json() == {'API': 'HELLO, HUMAN'}


async def test_delete_user():
    response = await test_asclient.delete('/users/{id}/', id=1, headers=[])
    assert response.status_code == 203
