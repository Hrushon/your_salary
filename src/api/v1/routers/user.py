from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.v1.request_models.user import (UserAuthenticateRequest,
                                            UserChangeStatusRequest,
                                            UserCreateRequest,
                                            UserResetPasswordRequest,
                                            UserSelfUpdateRequest,
                                            UserUpdateRequest)
from src.api.v1.response_models.error import generate_error_responses
from src.api.v1.response_models.user import (UserAndAccessTokenResponse,
                                             UserResponse, UserShortResponse)
from src.core.services.permissions import (is_administrator,
                                           is_administrator_or_staff)
from src.core.services.user_service import AuthenticationService, UserService

router = APIRouter(
    prefix='/employees',
    tags=['Работники'],
)


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary='Выполнить аутентификацию',
    response_description='Аутентификация выполнена',
    responses=generate_error_responses(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_403_FORBIDDEN
    )
)
async def login(
    auth_data: UserAuthenticateRequest,
    auth_service: Annotated[AuthenticationService, Depends()]
) -> UserAndAccessTokenResponse:
    """Аутентифицировать работника по `username` и паролю.

    Вернуть access-токен и информацию о работнике.
    - **username**: логин/никнейм работника
    - **password**: пароль
    """
    user_and_token = await auth_service.login_user(auth_data=auth_data)
    user_and_token.user.access_token = user_and_token.access_token
    return user_and_token.user


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Получить список всех работников',
    response_description='Получен список всех работников',
    responses=generate_error_responses(
        status.HTTP_403_FORBIDDEN,
    ),
    dependencies=(Depends(is_administrator_or_staff),)
)
async def get_users(
    user_service: Annotated[UserService, Depends()]
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
    return await user_service.get_all()


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
    user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    """
    Создает запись нового работника в базе данных.

    - **first_name**: имя работника
    - **last_name**: фамилия работника
    - **username**: логин/никнейм работника
    - **password**: пароль работника
    - **password_repeat**: повторный ввод пароля
    - **date_of_birth**: день рождения работника
    """
    return await user_service.create_user(data=data)


@router.get(
    '/me/',
    status_code=status.HTTP_200_OK,
    summary='Получить работником собственных данных из БД',
    response_description='Получены данные работником',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_401_UNAUTHORIZED
    )
)
async def get_user_by_self(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    auth_service: Annotated[AuthenticationService, Depends()],
) -> UserResponse:
    """Возвращает пользователю запись c его данными из базы."""
    return await auth_service.get_current_user(token=token)


@router.patch(
    '/me/',
    status_code=status.HTTP_200_OK,
    summary='Обновление работником собственных данных в БД',
    response_description='Обновлены данные работником',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def update_by_user_himself(
    data: UserSelfUpdateRequest,
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    user_service: Annotated[UserService, Depends()],
    auth_service: Annotated[AuthenticationService, Depends()]
) -> UserResponse:
    """
    Обновляет coбственную запись работника в базе данных.

    И возвращает данные обновленной записи.

    - **first_name**: имя работника
    - **last_name**: фамилия работника
    - **date_of_birth**: день рождения работника
    """
    user = await auth_service.get_current_user(token=token)
    return await user_service.update_user_himself(data=data, user_obj=user)


@router.get(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Получить данные отдельного работника из БД',
    response_description='Получены данные работника из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    ),
    dependencies=(Depends(is_administrator_or_staff),)
)
async def get_user_by_id(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    """
    Возвращает запись отдельного работника из базы данных по полю `id`.

    - **obj_id**: уникальный идентификатор записи в БД
    """
    return await user_service.get_by_id(obj_id=obj_id)


@router.patch(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Обновить данные работника в БД',
    response_description='Обновлены данные работника в БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    ),
    dependencies=(Depends(is_administrator_or_staff),)
)
async def update_user(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    data: UserUpdateRequest,
    user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    """
    Обновляет запись отдельного работника в базе данных по полю `id`.

    И возвращает данные обновленной записи.

    - **first_name**: имя работника
    - **last_name**: фамилия работника
    - **date_of_birth**: день рождения работника
    - **department**: идентификатор отдела в котором работает работник
    - **position**: идентификатор должности работника
    - **salary**: идентификатор заработной плата работника
    """
    return await user_service.update_user(obj_id=obj_id, data=data)


@router.patch(
    '/{obj_id}/status/',
    status_code=status.HTTP_200_OK,
    summary='Изменить статус работника в БД',
    response_description='Изменен статус работника в БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    ),
    dependencies=(Depends(is_administrator),)
)
async def change_user_status(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    data: UserChangeStatusRequest,
    user_service: Annotated[UserService, Depends()]
) -> UserShortResponse:
    """
    Изменяет статус отдельного работника в базе данных по полю `id`.

    Возвращает данные обновленной записи.

    - **obj_id**: уникальный идентификатор записи в БД
    - **status**: статус работника

    Варианты статусов:
        `admin` - администратор
        `staff` - управляющий персонал
        `employee` - работник без доступа к данным других работников
    """
    return await user_service.change_user_status(obj_id=obj_id, data=data)


@router.get(
    '/{obj_id}/block/',
    status_code=status.HTTP_200_OK,
    summary='Заблокировать работника',
    response_description='Работник заблокирован',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
    ),
    dependencies=(Depends(is_administrator_or_staff),)
)
async def block_user(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    """
    Блокирует работника по полю `id`.

    Возвращает данные заблокированной записи.

    - **obj_id**: уникальный идентификатор записи в БД
    """
    return await user_service.set_block_user(obj_id=obj_id)


@router.get(
    '/{obj_id}/unblock/',
    status_code=status.HTTP_200_OK,
    summary='Разблокировать работника',
    response_description='Работник разблокирован',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
    ),
    dependencies=(Depends(is_administrator_or_staff),)
)
async def unblock_user(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    """
    Снимает блокировку с работника по полю `id`.

    Возвращает данные заблокированной записи.

    - **obj_id**: уникальный идентификатор записи в БД
    """
    return await user_service.unset_block_user(obj_id=obj_id)


@router.patch(
    '/{obj_id}/password_reset/',
    status_code=status.HTTP_200_OK,
    summary='Изменение пароля работника в БД',
    response_description='Изменен пароль работника в БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    ),
    dependencies=(Depends(is_administrator),)
)
async def change_user_password(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    data: UserResetPasswordRequest,
    user_service: Annotated[UserService, Depends()]
) -> UserShortResponse:
    """
    Изменяет пароль отдельного работника в базе данных по полю `id`.

    Возвращает данные обновленной записи.

    - **obj_id**: уникальный идентификатор записи в БД
    - **password**: новый пароль работника
    - **password_repeat**: повторный ввод нового пароля работника
    """
    return await user_service.change_user_password(obj_id=obj_id, data=data)


@router.delete(
    '/{obj_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить данные работника из БД',
    response_description='Удалены данные работника из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    ),
    dependencies=(Depends(is_administrator_or_staff),)
)
async def delete_user(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    user_service: Annotated[UserService, Depends()]
) -> None:
    """Удаляет запись отдельного работника из базы данных по полю `id`."""
    return await user_service.delete_user(obj_id=obj_id)
