from http import HTTPStatus

from fastapi import APIRouter

from ..request_models.product import ProductRequest

router = APIRouter(
    prefix='/products',
    tags=['products'],
)


@router.post(
    '/create',
    status_code=HTTPStatus.CREATED,
    summary='Создать продукт в БД',
    response_description='Создан продукт в БД'
)
async def create_product(product: ProductRequest) -> ProductRequest:
    return product
