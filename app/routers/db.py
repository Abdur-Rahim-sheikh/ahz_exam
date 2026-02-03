import logging
from contextlib import asynccontextmanager
from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session, select, update

from ..core.database import session_scope
from ..dependencies.db_depends import get_session
from ..models import Author, Book
from ..schemas.author_schema import AuthorCreate
from ..schemas.book_schema import BookCreate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_authors():
    author_1 = Author(name="Deadpond", date_of_birth=date.today())
    author_2 = Author(name="spider-boy", date_of_birth=date.today() - timedelta(1))
    author_3 = Author(name="rusty-man", date_of_birth=date.today() - timedelta(2))
    author_4 = Author(name="busty-man", date_of_birth=date.today() - timedelta(3))
    author_5 = Author(name="crusty-man", date_of_birth=date.today() - timedelta(4))
    author_6 = Author(name="thirsty-man", date_of_birth=date.today() - timedelta(5))

    with session_scope() as session:
        session.add_all([author_1, author_2, author_3, author_4, author_5, author_6])
        session.commit()

        logger.debug(msg=f"{author_1=}, {author_2=}, {author_3=}")
        logger.debug(msg=f"{author_1=}, {author_2.name=}, {author_3=}")

        logger.debug(msg=f"{author_1=}, {author_2=}, {author_3=}")


def create_books():
    book_1 = Book(
        title="Nadu amar Nadu",
        author_id=1,
        published_date=date.today(),
        genre="romance",
    )
    book_2 = Book(
        title="Padu amar Padu", author_id=1, published_date=date.today(), genre="comedy"
    )
    book_3 = Book(
        title="Gandu amar Gandu",
        author_id=1234,
        published_date=date.today(),
        genre="horror",
    )
    with session_scope() as session:
        session.add_all([book_1, book_2, book_3])
        session.commit()


@asynccontextmanager
async def lifespan(_router: APIRouter):
    create_authors()
    create_books()
    yield


router = APIRouter(lifespan=lifespan)


@router.post("/create-author", tags=["Author"])
def create_author(
    request: AuthorCreate, session: Annotated[Session, Depends(get_session)]
):
    author = Author.model_validate(request)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/get-authors", tags=["Author"])
def get_authors(offset: int = 0, session: Session = Depends(get_session)):
    # statement = select(Author.name).where(or_(Author.id == 1, Author.id % 2 == 0))
    statement = select(Author.name).limit(3).offset(offset=offset)
    authors = session.exec(statement=statement).all()
    return authors


@router.get("/get-author/{id}", tags=["Author"])
def get_author_by_id(id: int, session: Session = Depends(get_session)):
    author = session.get(Author, id)
    return author


@router.get("/author/books/{author_name}", tags=["Author"])
def get_books(author_name: str, session: Annotated[Session, Depends(get_session)]):
    try:
        results = session.exec(select(Author).where(Author.name == author_name))
        author = results.first()
    except Exception as e:
        raise HTTPException("author not found") from e

    results = session.exec(select(Book).where(Book.author_id == author.id))
    books = results.all()
    return books


@router.post("/book/create", tags=["Book"])
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


@router.post("/book/update-title", tags=["Book"])
def update_book_title(
    id: Annotated[int, Body()],
    title: Annotated[str, Body()],
    session: Annotated[Session, Depends(get_session)],
):
    statement = update(Book).where(Book.id == id).values(title=title)
    session.exec(statement=statement)

    session.commit()
    return "OK"
