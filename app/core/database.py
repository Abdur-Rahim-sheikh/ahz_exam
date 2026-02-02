from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine

from ..models import Author, Book  # noqa

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@contextmanager
def session_scope():
    with Session(engine) as session:
        yield session
