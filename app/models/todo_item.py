from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class TodoItem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    content: str
    is_complete: bool = Field(default=False)

    