from http import HTTPStatus

from fastapi import APIRouter

from ..request_models.user import UserCreateRequest
from ..response_models.user import UserResponse

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    summary='Создать пользователя в БД',
    response_description='Создан пользователь в БД'
)
async def create_user(product: UserCreateRequest) -> UserResponse:
    return product
