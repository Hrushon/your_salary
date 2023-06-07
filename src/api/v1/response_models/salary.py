from datetime import date

from pydantic import BaseModel

from .user import UserNestedResponse


class SalaryResponse(BaseModel):
    id: int
    amount: float
    raise_date: date
    employee: UserNestedResponse | None

    class Config:
        orm_mode = True
