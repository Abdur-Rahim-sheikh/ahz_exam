from sqlmodel import Date, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class Author(SQLModel, table=True):
    name: str
    date_of_birth: Date


class Book(SQLModel, table=True):
    title: str
    author: Author
    published_date: Date
    genre: str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
