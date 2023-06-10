from httpx import AsyncClient

from .conftest import dependency_overrides


@dependency_overrides
async def test_read_departments(aclient: AsyncClient):
    response = await aclient.get('/departments/')
    assert response.status_code == 200
    assert response.json() == []


@dependency_overrides
async def test_create_department(aclient: AsyncClient):
    response = await aclient.post(
        '/departments/', json={'title': 'Текущий ремонт'}
    )
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'title': 'Текущий ремонт',
        'employees': []
    }


@dependency_overrides
async def test_read_department_by_id(aclient: AsyncClient):
    response = await aclient.get('/departments/1/')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'title': 'Текущий ремонт',
        'employees': []
    }


@dependency_overrides
async def test_update_department(aclient: AsyncClient):
    response = await aclient.patch(
        '/departments/1/', json={'title': 'Экономический отдел'}
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'title': 'Экономический отдел',
        'employees': []
    }


@dependency_overrides
async def test_delete_department(aclient: AsyncClient):
    response = await aclient.delete('/departments/1/')
    assert response.status_code == 204
