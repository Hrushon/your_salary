from pydantic import BaseModel

from .user import UserResponse


class PositionResponse(BaseModel):
    title: str
    empoloyees: list[UserResponse] | None

    class Config:
        orm_mode = True
