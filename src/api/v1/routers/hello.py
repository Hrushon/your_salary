from fastapi import APIRouter, status

router = APIRouter(
    prefix='/checking',
    tags=['Проверка API'],
)


@router.get(
    '/hello_api',
    status_code=status.HTTP_200_OK,
    summary='Проверка работоспособности API',
    response_description='API работает'
)
async def hello_world():
    return {'API': 'HELLO, HUMAN'}
