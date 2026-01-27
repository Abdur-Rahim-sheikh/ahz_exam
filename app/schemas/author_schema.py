from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    date_of_birth: date


class AuthorCreate(AuthorBase):
    pass
