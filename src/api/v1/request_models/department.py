from pydantic import Field, StrictStr

from .base_request import BaseRequest
from .validators import department_position_validator


class DepartmentCreateRequest(BaseRequest):
    title: StrictStr = Field(min_length=2, max_length=256)

    _validate_title = department_position_validator('title')


class DepartmentUpdateRequest(BaseRequest):
    title: StrictStr | None = Field(min_length=2, max_length=256)

    _validate_title = department_position_validator('title')
