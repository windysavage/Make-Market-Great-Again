from collections.abc import Generator
from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = 'mysql+pymysql://admin:admin@mysql:3306/mmga'
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
