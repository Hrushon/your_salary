from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter(
    prefix='/checking',
    tags=['checking'],
)


@router.get(
    '/hello_api',
    status_code=HTTPStatus.OK,
    summary='Проверка работоспособности API',
    response_description='API работает'
)
async def hello_world():
    return {'API': 'HELLO, HUMAN'}
