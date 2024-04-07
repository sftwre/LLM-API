"""Main project file"""

import asyncio
import random

from uuid import uuid4
from fastapi import FastAPI, HTTPException

from sse_starlette.sse import EventSourceResponse

# see llm.py to better understand the interaction with OpenAI's Chat Completion service.
from llm import prompt_llm_async
from data import Chat

app = FastAPI()
sessions = dict()


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


@app.post("/chat")
async def chat_completion(chat: Chat):

    username = chat.username
    session_id = chat.session_id

    # create a new session if one doesn't exists
    if not session_id:
        session_id = uuid4().hex
        sessions[session_id] = username
        message = (
            f"Welcome to the chat service {username}!. Your session id: {session_id}"
        )

    elif session_id in sessions:
        username = sessions[session_id]
        message = f"Hello again {username}!"
    else:
        raise HTTPException(status_code=404, detail=f"Invalid session id: {session_id}")

    return message


@app.put("/chat/{session_id}")
async def chat_continuation():
    pass


@app.get("/history/{session_id}")
async def show_chat_history(session_id: int):
    return f"Session ID: {session_id.int}"


@app.get("/")
async def home():
    return "hello world!"
