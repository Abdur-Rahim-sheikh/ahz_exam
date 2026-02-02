from datetime import date

from sqlmodel import (
    TIMESTAMP,
    Column,
    Field,
    SQLModel,
    text,
)


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    date_of_birth: date
    # books: list["Book"] = Relationship(back_populates="author")


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(default=None, foreign_key="author.id")
    # author: Author = Relationship(back_populates="books")
    published_date: date = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    genre: str
    is_archived: bool = False
