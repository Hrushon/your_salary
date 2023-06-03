from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from src.api.v1.request_models.user import UserCreateRequest, UserUpdateRequest
from src.api.v1.response_models.error import generate_error_responses
from src.api.v1.response_models.user import UserResponse
from src.core.services.users_service import UsersService

router = APIRouter(
    prefix='/employees',
    tags=['Работники'],
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Получить список всех работников',
    response_description='Получен список всех работников'
)
async def get_users(
    service: Annotated[UsersService, Depends()]
) -> list[UserResponse]:
    """
    Возвращает список всех работников из базы данных.

    - **id**: уникальный идентификатор записи в БД
    - **first_name**: имя работника
    - **last_name**: фамилия работника
    - **username**: логин/никнейм работника
    - **date_of_birth**: день рождения работника
    - **is_blocked**: блокировка работника
    - **status**: статус работника
    - **department**: отдел в котором работает работник
    - **position**: должность работника
    - **salary**: заработная плата работника
    """
    return await service.get_all()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Создать запись с работником в БД',
    response_description='Создана запись с работником в БД',
    responses=generate_error_responses(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def create_user(
    data: UserCreateRequest,
    service: Annotated[UsersService, Depends()],
) -> UserResponse:
    """
    Создает запись нового работника в базе данных.

    - **id**: уникальный идентификатор записи в БД
    - **first_name**: имя работника
    - **last_name**: фамилия работника
    - **username**: логин/никнейм работника
    - **date_of_birth**: день рождения работника
    - **department_id**: идентификатор отдела в котором работает работник
    - **position_id**: идентификатор должности работника
    - **salary_id**: идентификатор заработной плата работника
    """
    return await service.create_user(data=data)


@router.get(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Получить данные отдельного работника из БД',
    response_description='Получены данные работника из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def get_user_by_id(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[UsersService, Depends()],
) -> UserResponse:
    """
    Возвращает запись отдельного работника из базы данных по полю `id`.

    - **id**: уникальный идентификатор записи в БД
    - **first_name**: имя работника
    - **last_name**: фамилия работника
    - **username**: логин/никнейм работника
    - **date_of_birth**: день рождения работника
    - **is_blocked**: блокировка работника
    - **status**: статус работника
    - **department**: отдел в котором работает работник
    - **position**: должность работника
    - **salary**: заработная плата работника
    """
    return await service.get_by_id(obj_id=obj_id)


@router.patch(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Обновить данные работника в БД',
    response_description='Обновлены данные работника в БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def update_user(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    data: UserUpdateRequest,
    service: Annotated[UsersService, Depends()],
) -> UserResponse:
    """
    Обновляет запись отдельного работника в базе данных по полю `id`.

    И возвращает данные обновленной записи.

    - **id**: уникальный идентификатор записи в БД
    - **first_name**: имя работника
    - **last_name**: фамилия работника
    - **username**: логин/никнейм работника
    - **date_of_birth**: день рождения работника
    - **department_id**: идентификатор отдела в котором работает работник
    - **position_id**: идентификатор должности работника
    - **salary_id**: идентификатор заработной плата работника
    """
    return await service.update_user(obj_id=obj_id, data=data)


@router.delete(
    '/{obj_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить данные работника из БД',
    response_description='Удалены данные работника из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def delete_user(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[UsersService, Depends()],
) -> None:
    """Удаляет запись отдельного работника из базы данных по полю `id`."""
    return await service.delete_user(obj_id=obj_id)
