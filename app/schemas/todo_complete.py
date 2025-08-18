from pydantic import BaseModel


class TodoComplete(BaseModel):
    is_complete: bool