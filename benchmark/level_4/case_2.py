from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    number: int

    @field_validator('number', mode='after')  # (1)!
    @classmethod
    def is_even(cls, value: int) -> int:
        if value % 2 == 1:
            raise ValueError(f'{value} is not an even number')
        return value  # (2)!
