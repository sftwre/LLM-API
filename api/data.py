import json
from typing import List, Dict
from pydantic import BaseModel


class Chat(BaseModel):
    payload: str
    session_id: str | None = None
    username: str | None = None
    message_history: List[Dict] | None = None


def serialize(message_history: List[Dict]) -> str:
    """
    Converts message_history data structure into a json object for storage within Redis cache.

    :param message_history (List[Dict]): List of dictionaries, where each dictionary contains a `role` and `content` key for the chat.
    :returns: JSON representation of message_history.
    """
    return json.dumps(message_history)


def deserialize(serialized_history: str) -> List[Dict]:
    """
    Converts JSON string into List of Dictionaries that contain the message history.

    :param serialized_history (str): JSON representation of the message history in Redis
    :returns: List of Dictionaries with the message history.
    """
    return json.loads(serialized_history)
