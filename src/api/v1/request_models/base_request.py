from pydantic import BaseModel, Extra


class BaseRequest(BaseModel):

    class Config:
        extra = Extra.forbid
