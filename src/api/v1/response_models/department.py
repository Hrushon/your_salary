from pydantic import BaseModel

from .user import UserNestedResponse


class DepartmentResponse(BaseModel):
    id: int
    title: str
    empoloyees: list[UserNestedResponse] | None

    class Config:
        orm_mode = True
