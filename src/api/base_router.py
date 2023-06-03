from fastapi import APIRouter

from src.api.v1 import routers

router = APIRouter(
    prefix='/api/v1',
    responses={404: {'description': 'Ничего не найдено'}},
)

router.include_router(routers.checking_router)
router.include_router(routers.departments_router)
router.include_router(routers.positions_router)
