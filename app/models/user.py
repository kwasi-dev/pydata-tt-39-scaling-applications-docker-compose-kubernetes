from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    full_name: str
    email: str = Field(unique=True)
    password: str

    