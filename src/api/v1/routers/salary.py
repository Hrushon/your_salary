from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from pydantic import FutureDate

from src.api.v1.request_models.salary import (SalaryCreateRequest,
                                              SalaryUpdateRequest)
from src.api.v1.response_models.error import generate_error_responses
from src.api.v1.response_models.salary import SalaryResponse
from src.core.services.permissions import is_administrator_or_staff
from src.core.services.salary_service import SalaryService

router = APIRouter(
    prefix='/salaries',
    tags=['Заработные платы'],
    dependencies=(Depends(is_administrator_or_staff),)
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Получить список всех заработных плат',
    response_description='Получен список всех заработных плат'
)
async def get_salaries(
    service: Annotated[SalaryService, Depends()],
    date_after: FutureDate | None = None,
    date_before: FutureDate | None = None
) -> list[SalaryResponse]:
    """
    Возвращает список всех заработных плат из базы данных.

    Query-параметры `date_before` и `date_after` позволяют
    фильтровать результаты запроса по датам.
    - **`date_after`** - выводит результаты с датой `raise_date` больше
    или равной указанной.
    - **`date_before`** - выводит результаты с датой `raise_date` меньше
    или равной указанной.
    Порядок сортировки результатов определен
    по дате - от ближайшей даты к более поздней.

    - **id**: уникальный идентификатор записи в БД
    - **amount**: размер заработной платы
    - **raise_date**: дата следующего повышения заработной платы
    - **employee**: работник с такой заработной платой
    """
    return await service.get_all(
        date_after=date_after,
        date_before=date_before
    )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Создать запись с заработной платой в БД',
    response_description='Создана запись с заработной платой в БД',
    responses=generate_error_responses(
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def create_salary(
    data: SalaryCreateRequest,
    service: Annotated[SalaryService, Depends()],
) -> SalaryResponse:
    """
    Создает запись новой заработной платы в базе данных.

    - **id**: уникальный идентификатор записи в БД
    - **amount**: размер заработной платы
    - **raise_date**: дата следующего повышения заработной платы
    """
    return await service.create_salary(data=data)


@router.get(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Получить данные отдельной заработной платы из БД',
    response_description='Получены данные заработной платы из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def get_salary_by_id(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[SalaryService, Depends()],
) -> SalaryResponse:
    """
    Возвращает запись отдельной заработной платы из базы данных по полю `id`.

    - **id**: уникальный идентификатор записи в БД
    - **amount**: размер заработной платы
    - **raise_date**: дата следующего повышения заработной платы
    - **employee**: работник с такой заработной платой
    """
    return await service.get_by_id(obj_id=obj_id)


@router.patch(
    '/{obj_id}/',
    status_code=status.HTTP_200_OK,
    summary='Обновить данные заработной платы в БД',
    response_description='Обновлены данные заработной платы в БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def update_salary(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    data: SalaryUpdateRequest,
    service: Annotated[SalaryService, Depends()],
) -> SalaryResponse:
    """
    Обновляет запись отдельной заработной платы в базе данных по полю `id`.

    И возвращает данные обновленной записи.

    - **id**: уникальный идентификатор записи в БД
    - **amount**: размер заработной платы
    - **raise_date**: дата следующего повышения заработной платы
    """
    return await service.update_salary(obj_id=obj_id, data=data)


@router.delete(
    '/{obj_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить данные заработной платы из БД',
    response_description='Удалены данные заработной платы из БД',
    responses=generate_error_responses(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY
    )
)
async def delete_salary(
    obj_id: Annotated[int, Path(description='Значение поля id записи', gt=0)],
    service: Annotated[SalaryService, Depends()],
) -> None:
    """Удаляет запись отдельной зарплаты из базы данных по полю `id`."""
    return await service.delete_salary(obj_id=obj_id)
