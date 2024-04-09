from pydantic import BaseModel


class Chat(BaseModel):
    payload: str
