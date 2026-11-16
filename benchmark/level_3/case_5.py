from pydantic import BaseModel


class Hobby(BaseModel):
    name: str
    info: str


class User(BaseModel):
    hobbies: list[Hobby]
