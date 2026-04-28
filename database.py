from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends

engine = create_engine("sqlite:///notes.db")

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
