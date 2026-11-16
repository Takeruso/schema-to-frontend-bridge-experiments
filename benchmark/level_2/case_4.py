from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    x: int = Field(multiple_of=5)
