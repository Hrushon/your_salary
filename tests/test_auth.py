import pytest
from httpx import AsyncClient

from .conftest import create_auth_needs_data  # noqa


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


async def test_auth_bad_token(aclient: AsyncClient, get_tokens: dict):
    response = await aclient.get('/employees/', headers={
        'Authorization': 'Bearer sdfm;sdklgjkl;sdjglk'
    })
    assert response.status_code == 401


async def test_auth_read_users(aclient: AsyncClient, get_tokens: dict):
    response = await aclient.get('/employees/')
    assert response.status_code == 403
    response = await aclient.get('/employees/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403
    response = await aclient.get('/employees/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 200
    response = await aclient.get('/employees/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    assert response.status_code == 200


async def test_auth_read_users_by_id(aclient: AsyncClient, get_tokens: dict):
    response = await aclient.get('/employees/1/')
    assert response.status_code == 403
    response = await aclient.get('/employees/1/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403
    response = await aclient.get('/employees/1/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 200
    response = await aclient.get('/employees/1/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    assert response.status_code == 200


async def test_auth_update_user_by_id(aclient: AsyncClient, get_tokens: dict):
    data = {
        'first_name': 'Иван',
        'last_name': 'Иванов'
    }
    response = await aclient.patch('/employees/1/', json=data)
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['employee'])
        }
    )
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['staff'])
        }
    )
    assert response.status_code == 200
    response = await aclient.patch(
        '/employees/1/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['admin'])
        }
    )
    assert response.status_code == 200


async def test_auth_update_user_status_by_id(
    aclient: AsyncClient, get_tokens: dict
):
    data = {
        'status': 'admin'
    }
    response = await aclient.patch('/employees/1/status/', json=data)
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/status/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['employee'])
        }
    )
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/status/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['staff'])
        }
    )
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/status/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['admin'])
        }
    )
    assert response.status_code == 200


async def test_auth_block_user_by_id(
    aclient: AsyncClient, get_tokens: dict
):
    response = await aclient.get('/employees/1/block/')
    assert response.status_code == 403
    response = await aclient.get('/employees/1/block/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403
    response = await aclient.get('/employees/1/block/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 200
    response = await aclient.get('/employees/1/block/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    assert response.status_code == 200


async def test_auth_unblock_user_by_id(
    aclient: AsyncClient, get_tokens: dict
):
    response = await aclient.get('/employees/1/unblock/')
    assert response.status_code == 403
    response = await aclient.get('/employees/1/unblock/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403
    response = await aclient.get('/employees/1/unblock/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 200
    response = await aclient.get('/employees/1/unblock/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    assert response.status_code == 200


async def test_auth_reset_user_password_by_id(
    aclient: AsyncClient, get_tokens: dict
):
    data = {
        'password': '123456789',
        'password_repeat': '123456789'
    }
    response = await aclient.patch('/employees/1/password_reset/', json=data)
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/password_reset/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['employee'])
        }
    )
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/password_reset/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['staff'])
        }
    )
    assert response.status_code == 403
    response = await aclient.patch(
        '/employees/1/password_reset/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['admin'])
        }
    )
    assert response.status_code == 200


async def test_auth_delete_user_by_id(
    aclient: AsyncClient, get_tokens: dict
):
    response = await aclient.delete('/employees/3/')
    assert response.status_code == 403
    response = await aclient.delete('/employees/3/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403
    response = await aclient.delete('/employees/3/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 204
    response = await aclient.delete('/employees/2/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    assert response.status_code == 204
