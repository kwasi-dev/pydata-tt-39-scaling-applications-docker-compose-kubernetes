from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class TokenBlacklist(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    token:str
    