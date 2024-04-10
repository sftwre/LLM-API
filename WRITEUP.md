# Chat API service
The API has three main routes

- /
  - Default home route used to initiate a chat session and retrieve the session id
- /chat/{session_id}
  - Core chat route used to query the GPT-3.5-turbo model and receive a SSE response
- /chat_history/{session_id}
  - This route is used to retrieve the complete dialouge for a given session. Both client prompts and AI responses are returned.

## Launching service

To launch the service
1. Create a `.env` file in the project's default directory and add your OPENAI_API_KEY
   `vim .env`,
   `OPENAI_API_KEY=<key>`
2. Build the docker image using the following command in the default directory.
   `docker build -t chat_api_service .`
3. Launch docker container using the following command
   `docker run -d -p 8000:8000 chat_api_service`

## API usage
Follow this flow to utilize the API

1. Initiate chat session and retrieve session id
   `curl http://127.0.0.1:8000?username=TR`
2. Send prompts to API
   `curl -X PUT http://127.0.0.1:8000/chat/<session_id> -H "Content-Type: application/json" -d '{"payload": "Hello! What is your name?"}'`
3. Get chat history
   `curl http://127.0.0.1:8000/chat_history/<session_id>`

Alternatively, a better tool to ping the API would be [Postman](https://www.postman.com/); This is the tool I utilized during development.

## Running tests

Launch the docker container in interactive mode to run the test suite. The Redis server and Uvicorn servers must be running for the tests to execute.

1. Launch container in interactive mode
`docker run -it --rm -p 8000:8000 --entrypoint bash chat_api_service`
2. Execute `launch.sh` as a background process
`./launch.sh &`
3. Run test suite
`python -m pytest tests`

## Future work

I did not have time to resolve this error within `test_chat_history()`: *FAILED tests/test_main.py::test_chat_history - RuntimeError: <asyncio.locks.Event object at 0x7f4376ab08e0 [unset]> is bound to a different event loop*
A possible solution involves using this library: https://github.com/vinissimus/async-asgi-testclient
See this Stackoverflow post for more info: https://stackoverflow.com/questions/72715083/pytest-asyncio-event-is-bound-to-a-different-event-loop-event-loop-is-closed

Future enhancements to the API include
- Building a front-end with Streamlit, see this repo for reference https://github.com/sftwre/Chatbot.
- Create a route to retreive all existing sessions for a given username.
- Create prompts to initiate a 90s sitcom trivia game with the client. Information on shows can pulled from [Fandom](https://seinfeld.fandom.com/wiki/Seinfeld) and utilized by the LLM to create trivia questions via RAG.