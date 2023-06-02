from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.v1.request_models.department import (DepartmentCreateRequest,
                                                  DepartmentUpdateRequest)
from src.api.v1.response_models.department import DepartmentResponse
from src.core.services.departments_servise import DepartmentsService

router = APIRouter(
    prefix='/departments',
    tags=['departments'],
)


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    summary='Получить список всех департаментов',
    response_description='Получен список всех департаментов'
)
async def get_departments(
    service: Annotated[DepartmentsService, Depends()]
) -> list[DepartmentResponse]:
    return await service.get_all()


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    summary='Создать департамент в БД',
    response_description='Создан департамент в БД'
)
async def create_departament(
    data: DepartmentCreateRequest,
    service: Annotated[DepartmentsService, Depends()],
) -> DepartmentResponse:
    return await service.create_department(data=data)


@router.patch(
    '/{obj_id}/',
    status_code=HTTPStatus.OK,
    summary='Обновить данные департамента в БД',
    response_description='Обновленны данные департамента в БД'
)
async def update_departament(
    obj_id: int,
    data: DepartmentUpdateRequest,
    service: Annotated[DepartmentsService, Depends()],
) -> DepartmentResponse:
    return await service.update_department(obj_id=obj_id, data=data)


@router.delete(
    '/{obj_id}/',
    status_code=HTTPStatus.NO_CONTENT,
    summary='Удалить данные департамента из БД',
    response_description='Удалены данные департамента из БД'
)
async def delete_departament(
    obj_id: int,
    service: Annotated[DepartmentsService, Depends()],
) -> None:
    return await service.delete_department(obj_id=obj_id)
