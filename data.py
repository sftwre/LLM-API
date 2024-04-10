import json
from typing import List, Dict
from pydantic import BaseModel


class Chat(BaseModel):
    payload: str
    session_id: str | None = None
    username: str | None = None
    message_history: List[Dict] | None = None


def serialize(message_history: List[Dict]) -> str:
    return json.dumps(message_history)


def deserialize(serialized_history: str) -> List[Dict]:
    return json.loads(serialized_history)
