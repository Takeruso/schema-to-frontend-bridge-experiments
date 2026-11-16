from typing import Any

from pydantic import BaseModel, field_validator


class Model(BaseModel):
    number: int

    @field_validator('number', mode='plain')
    @classmethod
    def val_number(cls, value: Any) -> Any:
        if isinstance(value, int):
            return value * 2
        else:
            return value
