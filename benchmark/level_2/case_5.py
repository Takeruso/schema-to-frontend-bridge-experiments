from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    x: str = Field(pattern='test')
