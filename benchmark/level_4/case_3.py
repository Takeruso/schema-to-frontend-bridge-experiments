from typing import Any

from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    numbers: list[int]

    @field_validator('numbers', mode='before')
    @classmethod
    def ensure_list(cls, value: Any) -> Any:  # (1)!
        if not isinstance(value, list):  # (2)!
            return [value]
        else:
            return value
