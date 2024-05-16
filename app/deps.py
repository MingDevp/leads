from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine
from pydantic_core import MultiHostUrl

SQLALCHEMY_DATABASE_URI = MultiHostUrl.build(
    scheme="postgresql+psycopg",
    username="postgres",
    password="",
    host="db",
    port=5432,
    path="app",
)

engine = create_engine(str(SQLALCHEMY_DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
