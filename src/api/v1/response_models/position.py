from pydantic import BaseModel

from .user import UserNestedResponse


class PositionResponse(BaseModel):
    id: int
    title: str
    employees: list[UserNestedResponse] | None

    class Config:
        orm_mode = True
