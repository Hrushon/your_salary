from httpx import AsyncClient

from .conftest import dependency_overrides


@dependency_overrides
async def test_read_positions(aclient: AsyncClient):
    response = await aclient.get('/positions/')
    assert response.status_code == 200
    assert response.json() == []


@dependency_overrides
async def test_create_position(aclient: AsyncClient):
    response = await aclient.post('/positions/', json={'title': 'Уборщик'})
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'title': 'Уборщик',
        'employees': []
    }


@dependency_overrides
async def test_read_position_by_id(aclient: AsyncClient):
    response = await aclient.get('/positions/1/')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'title': 'Уборщик',
        'employees': []
    }


@dependency_overrides
async def test_update_position(aclient: AsyncClient):
    response = await aclient.patch('/positions/1/', json={'title': 'Менеджер'})
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'title': 'Менеджер',
        'employees': []
    }


@dependency_overrides
async def test_delete_position(aclient: AsyncClient):
    response = await aclient.delete('/positions/1/')
    assert response.status_code == 204
