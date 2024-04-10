"""Main project file"""

import asyncio
import random

from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends

from sse_starlette.sse import EventSourceResponse

# see llm.py to better understand the interaction with OpenAI's Chat Completion service.
from llm import prompt_llm
from data import Chat, serialize, deserialize
from database import get_redis_client, create_redis_key

app = FastAPI()
sessions = dict()
messages_db = dict()

RETRY_TIMEOUT = 5  # seconds


@app.get("/stream-example")
async def stream_example():
    """
    Example route for streaming text to the client, one word/token at a time.
    """

    async def stream_tokens():
        """
        Placeholder implementation for token streaming. Try running this route as-is to better understand how to
        stream data using Server-Sent Events (SSEs) in FastAPI.
        See this tutorial for more information: https://devdojo.com/bobbyiliev/how-to-use-server-sent-events-sse-with-fastapi
        """
        for token in ["hello", ", ", "this ", "is ", "a ", "streamed ", "response."]:
            # fake delay:
            await asyncio.sleep(random.randint(0, 3))

            print(f"Yielding token: {token}")
            yield token

    return EventSourceResponse(stream_tokens())


@app.put("/chat/{session_id}")
async def chat_completion(
    chat: Chat, session_id: str, redis_client=Depends(get_redis_client)
):

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
async def get_chat_history(session_id: str, redis_client=Depends(get_redis_client)):

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

    user_profile = {"username": curr_user, "session_id": session_id}

    return {
        **user_profile,
        "messages": message_history,
    }


@app.get("/")
async def home(username: str, redis_client=Depends(get_redis_client)):
    session_id = uuid4().hex
    redis_client.set(session_id, username)
    return f"Welcome to the chat service {username}!. Your session id: {session_id}"
