from typing import Annotated

from fastapi import Depends

from src.api.v1.request_models.user import UserCreateRequest, UserUpdateRequest
from src.data_base.crud import (DepartmentCRUD, PositionCRUD, SalaryCRUD,
                                UserCRUD)
from src.data_base.models import User


class UsersService:
    def __init__(
        self,
        user_crud: Annotated[UserCRUD, Depends()],
        department_crud: Annotated[DepartmentCRUD, Depends()],
        salary_crud: Annotated[SalaryCRUD, Depends()],
        position_crud: Annotated[PositionCRUD, Depends()],
    ) -> None:
        self.__crud = user_crud
        self.__department_crud = department_crud
        self.__salary_crud = salary_crud
        self.__position_crud = position_crud

    async def __get_nested_instances(
        self, data: UserCreateRequest
    ) -> UserCreateRequest:
        """Получает объекты связываемых экземпляров моделей по `id`.

        Аргументы:
            data: UserCreateRequest - данные для создания объекта.
        """
        if data.department:
            data.department = await self.__department_crud.get_or_404(
                data.department
            )
        if data.position:
            data.position = await self.__position_crud.get_or_404(
                data.position
            )
        if data.salary:
            data.salary = await self.__salary_crud.get_or_404(
                data.salary
            )
        return data

    async def get_all(self) -> list[User]:
        """Возвращает список всех пользователей из БД."""
        return await self.__crud.get_all()

    async def create_user(
        self, data: UserCreateRequest
    ) -> User:
        """Создает запись с новым пользователем в БД.

        Аргументы:
            data: UserCreateRequest - данные для создания объекта.
        """
        data = await self.__get_nested_instances(data=data)
        user = User(**data.dict())
        return await self.__crud.create(user)

    async def get_by_id(
        self, obj_id: int
    ) -> User:
        """Возвращает отдельную запись с пользователем из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.get_or_404(obj_id=obj_id)

    async def update_user(
        self, obj_id: int, data: UserUpdateRequest
    ) -> User:
        """Обновляет данные записи с пользователем в БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД,
            data: UserUpdateRequest - данные для создания объекта.
        """
        data = await self.__get_nested_instances(data=data)
        data_dict = data.dict(exclude_unset=True)
        return await self.__crud.update(obj_id, data_dict)

    async def delete_user(self, obj_id: int) -> None:
        """Удаляет запись с данными пользователя из БД.

        Аргументы:
            obj_id: int - значение поля `id` записи в БД.
        """
        return await self.__crud.delete(obj_id)
