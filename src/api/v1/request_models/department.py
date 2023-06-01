from pydantic import StrictStr, Field

from .base_request import BaseRequest
from .validators import department_position_validator


class DepartmentCreateRequest(BaseRequest):
    title: StrictStr = Field(min_length=2, max_length=256)

    _validate_title = department_position_validator('title')
