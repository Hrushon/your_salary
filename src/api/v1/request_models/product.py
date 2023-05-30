from pydantic import BaseModel, Field, PositiveInt


class ProductRequest(BaseModel):
    title: str = Field(min_length=2)
    count: PositiveInt
