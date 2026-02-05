from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author_id: int | None = None
    published_date: date
    genre: str


class BookCreate(BookBase):
    pass
