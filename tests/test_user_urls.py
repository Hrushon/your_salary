from httpx import AsyncClient

from .conftest import dependency_overrides, raise_date


@dependency_overrides
async def test_read_users(aclient: AsyncClient):
    response = await aclient.get('/employees/')
    assert response.status_code == 200
    assert response.json() == []


@dependency_overrides
async def test_create_user(aclient: AsyncClient):
    response = await aclient.post('/employees/', json={
        'first_name': 'Тест',
        'last_name': 'Тестович',
        'username': 'test',
        'password': '12345678',
        'password_repeat': '12345678',
        'date_of_birth': '1990-01-01'
    })
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'first_name': 'Тест',
        'last_name': 'Тестович',
        'username': 'test',
        'date_of_birth': '1990-01-01',
        'is_blocked': True,
        'status': 'employee',
        'department': None,
        'position': None,
        'salary': None
    }


@dependency_overrides
async def test_login_user_employee_blocked(aclient: AsyncClient):
    response = await aclient.post('/employees/login/', json={
        'username': 'test',
        'password': '12345678'
    })
    assert response.status_code == 403


@dependency_overrides
async def test_read_user_by_id(aclient: AsyncClient):
    response = await aclient.get('/employees/1/')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Тест',
        'last_name': 'Тестович',
        'username': 'test',
        'date_of_birth': '1990-01-01',
        'is_blocked': True,
        'status': 'employee',
        'department': None,
        'position': None,
        'salary': None
    }


@dependency_overrides
async def test_update_user(aclient: AsyncClient, create_user_needs_data: None):
    response = await aclient.patch('/employees/1/', json={
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'date_of_birth': '1995-01-01',
        'department': 1,
        'position': 1,
        'salary': 1
    })
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'username': 'test',
        'date_of_birth': '1995-01-01',
        'is_blocked': True,
        'status': 'employee',
        'department': {
            'id': 1,
            'title': 'Тестовый отдел'
        },
        'position': {
            'id': 1,
            'title': 'Тестовая должность'
        },
        'salary': {
            'id': 1,
            'amount': 99999.99,
            'raise_date': raise_date.strftime('%Y-%m-%d')
        }
    }


@dependency_overrides
async def test_update_status_user(aclient: AsyncClient):
    response = await aclient.patch('/employees/1/status/', json={
        'status': 'admin'
    })
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'username': 'test',
        'is_blocked': True,
        'status': 'admin'
    }


@dependency_overrides
async def test_unblock_user_by_id(aclient: AsyncClient):
    response = await aclient.get('/employees/1/unblock/')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'username': 'test',
        'is_blocked': False,
        'status': 'admin'
    }


@dependency_overrides
async def test_login_user_admin_unblocked(aclient: AsyncClient):
    response = await aclient.post('/employees/login/', json={
        'username': 'test',
        'password': '12345678'
    })
    assert response.status_code == 200


@dependency_overrides
async def test_read_self_user_with_token(aclient: AsyncClient):
    token = await aclient.post('/employees/login/', json={
        'username': 'test',
        'password': '12345678'
    })
    token = token.json()['access_token']
    response = await aclient.get('/employees/me/', headers={
        'Authorization': 'Bearer {}'.format(token)
    })
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'username': 'test',
        'date_of_birth': '1995-01-01',
        'is_blocked': False,
        'status': 'admin',
        'department': {
            'id': 1,
            'title': 'Тестовый отдел'
        },
        'position': {
            'id': 1,
            'title': 'Тестовая должность'
        },
        'salary': {
            'id': 1,
            'amount': 99999.99,
            'raise_date': raise_date.strftime('%Y-%m-%d')
        }
    }


@dependency_overrides
async def test_update_self_user_with_token(aclient: AsyncClient):
    token = await aclient.post('/employees/login/', json={
        'username': 'test',
        'password': '12345678'
    })
    token = token.json()['access_token']
    response = await aclient.patch(
        '/employees/me/',
        json={
            'first_name': 'Петр',
            'last_name': 'Петров',
            'date_of_birth': '2000-01-01',
        },
        headers={
            'Authorization': 'Bearer {}'.format(token)
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Петр',
        'last_name': 'Петров',
        'username': 'test',
        'date_of_birth': '2000-01-01',
        'is_blocked': False,
        'status': 'admin',
        'department': {
            'id': 1,
            'title': 'Тестовый отдел'
        },
        'position': {
            'id': 1,
            'title': 'Тестовая должность'
        },
        'salary': {
            'id': 1,
            'amount': 99999.99,
            'raise_date': raise_date.strftime('%Y-%m-%d')
        }
    }


@dependency_overrides
async def test_block_user_by_id(aclient: AsyncClient):
    response = await aclient.get('/employees/1/block/')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Петр',
        'last_name': 'Петров',
        'username': 'test',
        'is_blocked': True,
        'status': 'admin'
    }


@dependency_overrides
async def test_update_password_user(aclient: AsyncClient):
    response = await aclient.patch('/employees/1/password_reset/', json={
        'password': '123456789',
        'password_repeat': '123456789'
    })
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'first_name': 'Петр',
        'last_name': 'Петров',
        'username': 'test',
        'is_blocked': True,
        'status': 'admin'
    }


@dependency_overrides
async def test_delete_user(aclient: AsyncClient):
    response = await aclient.delete('/employees/1/')
    assert response.status_code == 204
