from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.database import session_scope
from ..dependencies.db_depends import get_session
from ..models import Author, Book
from ..schemas.author_schema import AuthorCreate
from ..schemas.book_schema import BookCreate
from contextlib import asynccontextmanager
from datetime import date


def create_authors():
    author_1 = Author(name="Deadpond", date_of_birth=date.today())
    author_2 = Author(name="spider-boy", date_of_birth=date.today())
    author_3 = Author(name="rusty-man", date_of_birth=date.today())
    with session_scope() as session:
        session.add_all([author_1, author_2, author_3])
        session.commit()


@asynccontextmanager
async def lifespan(_router: APIRouter):
    create_authors()
    yield


router = APIRouter(lifespan=lifespan)


@router.post("/create-author")
def create_author(
    request: AuthorCreate, session: Annotated[Session, Depends(get_session)]
):
    author = Author.model_validate(request)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.post("/create-book")
def create_book(request: BookCreate, session: Annotated[Session, Depends(get_session)]):
    # try:
    #     results = session.exec(select(Author).where(Author.id == request.author_id))
    #     author = results.one()
    # except Exception as e:
    #     raise HTTPException(status_code=422, detail="author not found") from e
    book = Book.model_validate(request)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/author/books/{author_name}")
def get_books(author_name: str, session: Annotated[Session, Depends(get_session)]):
    try:
        results = session.exec(select(Author).where(Author.name == author_name))
        author = results.one()
    except Exception as e:
        raise HTTPException("author not found") from e

    results = session.exec(select(Book).where(Book.author_id == author.id))
    books = results.all()
    return books
