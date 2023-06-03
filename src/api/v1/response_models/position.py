from pydantic import BaseModel

from .user import UserNestedResponse


class PositionResponse(BaseModel):
    id: int
    title: str
    empoloyees: list[UserNestedResponse] | None

    class Config:
        orm_mode = True
