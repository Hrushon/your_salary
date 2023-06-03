from typing import Annotated

from fastapi import Depends

from src.api.v1.request_models.user import UserCreateRequest, UserUpdateRequest
from src.data_base.crud import UserCRUD
from src.data_base.models import User


class UsersService:
    def __init__(
        self, user_crud: Annotated[UserCRUD, Depends()]
    ) -> None:
        self._crud = user_crud

    async def get_all(self) -> list[User]:
        """Возвращает список всех пользователей из БД."""
        return await self._crud.get_all()

    async def create_user(
        self, data: UserCreateRequest
    ) -> User:
        """Создает запись с новым пользователем в БД.

        Аргументы:
            data: UserCreateRequest - данные для создания объекта.
        """
        user = User(**data.dict())
        return await self._crud.create(user)

    async def get_by_id(
        self, obj_id: int
    ) -> User:
        """Возвращает отдельную запись с пользователем из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self._crud.get_or_404(obj_id=obj_id)

    async def update_user(
        self, obj_id: int, data: UserUpdateRequest
    ) -> User:
        """Обновляет данные записи с пользователем в БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД,
            data: UserUpdateRequest - данные для создания объекта.
        """
        data_dict = data.dict(exclude_unset=True)
        return await self._crud.update(obj_id, data_dict)

    async def delete_user(self, obj_id: int) -> None:
        """Удаляет запись с данными пользователя из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self._crud.delete(obj_id)
