from typing import Dict, List
from pydantic import BaseModel


class Chat(BaseModel):
    username: str
    session_id: str | None = None
