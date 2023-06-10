import pytest
from httpx import AsyncClient


async def test_auth_bad_token(aclient: AsyncClient, get_tokens: dict):
    response = await aclient.get('/employees/', headers={
        'Authorization': 'Bearer sdfm;sdklgjkl;sdjglk'
    })
    assert response.status_code == 401


@pytest.mark.parametrize(
    'url', ['/departments/', '/positions/', '/salaries/']
)
async def test_auth_unauthenticated_user_access_secondary_obj(
    aclient: AsyncClient,
    get_tokens: dict,
    url: str
):
    data = {
        'title': 'Тест тест тест'
    }
    if url == '/salaries/':
        data = {
            'amount': 20000.98,
            'raise_date': '2030-01-01'
        }
    response = await aclient.post(url, json=data)
    assert response.status_code == 403
    response = await aclient.get(url)
    assert response.status_code == 403
    response = await aclient.get(url + '1/')
    assert response.status_code == 403
    response = await aclient.patch(url + '1/', json=data)
    assert response.status_code == 403
    response = await aclient.delete(url + '1/')
    assert response.status_code == 403


@pytest.mark.parametrize(
    'url', ['/departments/', '/positions/', '/salaries/']
)
async def test_auth_employee_access_secondary_obj(
    aclient: AsyncClient,
    get_tokens: dict,
    url: str
):
    data = {
        'title': 'Тест тест тест'
    }
    if url == '/salaries/':
        data = {
            'amount': 20000.98,
            'raise_date': '2030-01-01'
        }
    response = await aclient.post(
        url,
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['employee'])
        }
    )
    assert response.status_code == 403
    response = await aclient.get(url, headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403
    response = await aclient.get(url + '1/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403
    response = await aclient.patch(
        url + '1/',
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['employee'])
        }
    )
    assert response.status_code == 403
    response = await aclient.delete(url + '1/', headers={
        'Authorization': 'Bearer {}'.format(get_tokens['employee'])
    })
    assert response.status_code == 403


@pytest.mark.parametrize(
    'url', ['/departments/', '/positions/', '/salaries/']
)
async def test_auth_staff_access_secondary_obj(
    aclient: AsyncClient,
    get_tokens: dict,
    url: str
):
    data = {
        'title': 'Тест тест тест'
    }
    if url == '/salaries/':
        data = {
            'amount': 20000.98,
            'raise_date': '2030-01-01'
        }
    response = await aclient.post(
        url,
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['staff'])
        }
    )
    assert response.status_code == 201
    response = await aclient.get(url, headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 200
    id = str(response.json()[0]['id'])
    response = await aclient.get(url + id, headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 200
    response = await aclient.patch(
        url + id,
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['staff'])
        }
    )
    assert response.status_code == 200
    response = await aclient.delete(url + id, headers={
        'Authorization': 'Bearer {}'.format(get_tokens['staff'])
    })
    assert response.status_code == 204


@pytest.mark.parametrize(
    'url', ['/departments/', '/positions/', '/salaries/']
)
async def test_auth_admin_access_secondary_obj(
    aclient: AsyncClient,
    get_tokens: dict,
    url: str
):
    data = {
        'title': 'Тест тест тест'
    }
    if url == '/salaries/':
        data = {
            'amount': 20000.98,
            'raise_date': '2030-01-01'
        }
    response = await aclient.post(
        url,
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['admin'])
        }
    )
    assert response.status_code == 201
    response = await aclient.get(url, headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    id = str(response.json()[0]['id'])
    assert response.status_code == 200
    response = await aclient.get(url + id, headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    assert response.status_code == 200
    response = await aclient.patch(
        url + id,
        json=data,
        headers={
            'Authorization': 'Bearer {}'.format(get_tokens['admin'])
        }
    )
    assert response.status_code == 200
    response = await aclient.delete(url + id, headers={
        'Authorization': 'Bearer {}'.format(get_tokens['admin'])
    })
    assert response.status_code == 204


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
