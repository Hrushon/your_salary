from typing import Annotated

from fastapi import Depends

from src.api.v1.request_models.department import DepartmentCreateRequest
from src.data_base.crud import DepartmentCRUD
from src.data_base.models import Department


class DepartmentsService:
    def __init__(
        self, department_crud: Annotated[DepartmentCRUD, Depends()]
    ) -> None:
        self._crud = department_crud

    async def get_all(self) -> list[Department]:
        return await self._crud.get_all()

    async def create_department(
        self, data: DepartmentCreateRequest
    ) -> Department:
        department = Department(**data.dict())
        return await self._crud.create(department)

    async def update_department(
        self, obj_id: int, data: DepartmentCreateRequest
    ) -> Department:
        data_dict = data.dict(exclude_unset=True)
        return await self._crud.update(obj_id, data_dict)

    async def delete_department(self, obj_id: int) -> None:
        return await self._crud.delete(obj_id)
