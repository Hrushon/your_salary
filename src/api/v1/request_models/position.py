from pydantic import Field, StrictStr

from .base_request import BaseRequest
from .validators import department_position_validator


class PositionCreateRequest(BaseRequest):
    title: StrictStr = Field(min_length=2, max_length=100)

    _validate_title = department_position_validator('title')
