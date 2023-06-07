from pydantic import FutureDate, condecimal

from .base_request import BaseRequest


class SalaryCreateRequest(BaseRequest):
    amount: condecimal(gt=0, max_digits=9, decimal_places=2)
    raise_date: FutureDate


class SalaryUpdateRequest(BaseRequest):
    amount: condecimal(gt=0, max_digits=9, decimal_places=2) | None
    raise_date: FutureDate | None
