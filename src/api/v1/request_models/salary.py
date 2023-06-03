from pydantic import PastDate, condecimal

from .base_request import BaseRequest


class SalaryCreateRequest(BaseRequest):
    amount: condecimal(gt=0, max_digits=9, decimal_places=2)
    raise_date: PastDate


class SalaryUpdateRequest(BaseRequest):
    amount: condecimal(gt=0, max_digits=9, decimal_places=2) | None
    raise_date: PastDate | None
