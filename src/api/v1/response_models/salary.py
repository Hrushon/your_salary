from datetime import date

from pydantic import BaseModel, condecimal

from .user import UserResponse


class SalaryResponse(BaseModel):
    amount: condecimal(gt=0, max_digits=9, decimal_places=2)
    raise_date: date
    empoloyee: UserResponse | None

    class Config:
        orm_mode = True
