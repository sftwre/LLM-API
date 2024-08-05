"""Main project file"""

import asyncio
import random

from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends

from sse_starlette.sse import EventSourceResponse

# see llm.py to better understand the interaction with OpenAI's Chat Completion service.
from api.llm import prompt_llm
from api.data import Chat, serialize, deserialize
from api.database import get_redis_client, create_redis_key

app = FastAPI()

RETRY_TIMEOUT = 5  # seconds


@app.put("/chat/{session_id}")
async def chat_completion(
    chat: Chat, session_id: str, redis_client=Depends(get_redis_client)
) -> EventSourceResponse:
    """
    This route provides the core chat functionality for the API and allows clients to prompt
    an LLM. Both client prompts and AI responses are stored in a Redis cache, they're retreived for context before pinging the OpenAI API.

    :param chat (Chat): Prompt from client
    :param session_id (str): Session id issued by API
    :param redis_client: redis cache
    :returns: Returns Server Sent Event that streams result tokens from the OpenAI API.
    """

    prompt = chat.payload
    redis_key = create_redis_key("chat_history", session_id)

    # verify sesssion id
    curr_user = redis_client.get(session_id)
    if not curr_user:
        raise HTTPException(status_code=404, detail=f"Invalid session id: {session_id}")

    # pull existing message history and deserialize from JSON
    serialized_history = redis_client.get(redis_key)

    if serialized_history is None:
        message_history = []
    else:
        message_history = deserialize(serialized_history)

    async def stream_tokens(prompt: str):
        stream = prompt_llm(prompt, existing_messages=message_history)
        current_response = ""

        for chunk in stream:
            # skip empty chunks
            if len(chunk.choices) > 0:
                token = chunk.choices[0].delta.content
                if token and token is not None:
                    current_response += token
                    yield token

        # save user prompt and ai response
        message_history.append({"role": "user", "content": prompt})
        message_history.append({"role": "assistant", "content": current_response})
        redis_client.set(redis_key, serialize(message_history))

    return EventSourceResponse(stream_tokens(prompt))


@app.get("/chat_history/{session_id}")
async def get_chat_history(
    session_id: str, redis_client=Depends(get_redis_client)
) -> Chat:
    """
    This route is used to pull the chat history for any existing chat session.

    :param session_id (str): Session id for a chat between client and OpenAI
    :param redis_client: redis cache
    :returns: A chat with the retrieved user profile and message history included.
    """

    # verify sesssion id
    curr_user = redis_client.get(session_id)
    if not curr_user:
        raise HTTPException(status_code=404, detail=f"Invalid session id: {session_id}")

    redis_key = create_redis_key("chat_history", session_id)
    serialized_history = redis_client.get(redis_key)

    # non-existent history, return empty list
    if not serialized_history:
        message_history = []
    else:
        message_history = deserialize(serialized_history)

    chat = Chat(
        payload="",
        username=curr_user,
        session_id=session_id,
        message_history=message_history,
    )
    return chat


@app.get("/")
async def home(username: str, redis_client=Depends(get_redis_client)) -> dict:
    """
    Default API route that issues new clients a Session ID. This is the entrypoint to the API and must be called
    before initiaing a chat.

    :param username (str): username provided by client
    :param redis_client: redis cache
    :returns: Returns dictionary with issued session id a welcome message.
    """
    session_id = uuid4().hex
    redis_client.set(session_id, username)
    return {
        "message": f"Welcome to the chat service {username}!",
        "session_id": session_id,
    }
