from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..dependencies.db_depends import get_session
from ..models import Author
from ..schemas.author_schema import AuthorCreate

router = APIRouter()


@router.post("/create-author")
async def create_author(
    request: AuthorCreate, session: Annotated[Session, Depends(get_session)]
):
    author = Author.model_validate(request)
    session.add(author)
    session.commit()
    session.refresh()
    return author
