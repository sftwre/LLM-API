# SWE, Backend & Applied ML take-home assignment

The goal of this take-home assignment is to assess aptitude for back-end engineering with tools and technologies that we use every day:

- OpenAI Python SDK (making calls to GPT-3.5/4/etc)
- FastAPI (with streaming responses)
- Pydantic

While the project is much more simplified than our production codebase, it is very similar in many ways.

We also hope the assignment is fun and provides you with a more detailed look into day-to-day work in the role.

It's perfectly fine to use outside resources such Google, Stackoverflow, and even ChatGPT itself. 

If you do, we ask that you note it in a comment next to any code that needed referencing outside sources.

If you're going to use ChatGPT, use it _narrowly_, e.g. ask only specific questions about one part of the project.

DO NOT USE CHATGPT (OR SIMILAR TOOLS) TO COMPLETE THE ASSIGNMENT FOR YOU.

Be aware that we have run this assignment itself through ChatGPT several times and are keenly familiar with the kind of output it will provide.

## Assignment

In `main.py`, we have provided a shell of a FastAPI app. It includes one route that demonstrates streaming data using Server-Sent Events (SSEs)

In `llm.py`, we have provided some code for prompting the Large Language Model (LLM) both synchronously and asynchronously. The prompts can be left as-is for this assignment. But we want to see aptitude in calling the LLM API and properly handling the response. See https://platform.openai.com/docs/api-reference/chat and https://platform.openai.com/docs/guides/text-generation/chat-completions-api?lang=python for more information about OpenAI's Chat Completions service. See https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb for information about receiving streaming results.

Please modify the file (or add your own files and organize them in any way you like) such that:
- The API provides a barebones Chat service that a front-end client can use.
- The service should have the following capabilities:
    - an HTTP client can create a new chat session
    - given a chat session (e.g. its ID), an HTTP client can send a message on behalf of the user, and receive the "AI" response from the LLM.
    - responses from the AI should be streamed using the SSE mechanism mentioned above.
    - an HTTP client can also fetch the entire message history for a given session

You'll likely need some sort of persistence. It's 100% acceptable to store chat messages in memory, but if you want to show off, feel free to use any of SQLite, Postgres, Redis, or just flat files for persistence. If you do this, make sure the rest of the functional requirements are met.

Do not worry about things like user authentication or really any other production consideration not already mentioned above.

To run the code, you'll need Python 3.10.x (other versions might work, but the project was written against 3.10.7).

Install dependencies: `pip install requirements.txt`

Add OpenAI API keys to the environment. Use `.env.example` and/or `llm.py` as a guide. DO NOT INCLUDE API KEYS IN YOUR SUBMISSION. Please obtain your own keys from your own account. If you are unable to do this, let us know and we'll find an alternative approach.

Running the local server:
```
uvicorn main:app --reload
```

Running the LLM code (good way to learn about it):

```
python llm.py "hey who are you and what can you do for me?" 
```

Submit the completed assignment back to us as either a zip file via email or Greenhouse, or as a private git repository (or GitHub gist). DO NOT publish this assignment publicly.

## Evaluation

We're going to view the submission holistically, but evaluation will focus on several key areas:
- does the submission accomplish the required tasks?
- code quality: is the code well-organized, documented (e.g. docstrings), and easy-to-understand?
- use of types: we love typed Python at Casetext, and it works really well with FastAPI and Pydantic. For more info, see https://docs.python.org/3/library/typing.html.
- data safety and validity: are proper measures taken to ensure data validity is checked both statically (e.g. through typing) and at runtime? consider the validity of data returned from the LLM's function calls.
- sensibility: do the names and HTTP methods for the routes effectively convey their purpose?
- easy to operate: does the HTTP API make it easy for a client (e.g. HTML/JS web app) to provide a user interface?
- proper use of asynchronous and synchronous Python code.

A successful submission will hit most of the points above. 
A standout submission will hit all of the points above.
A stellar submission will also demonstrate innovation at the prompt-level (e.g. modify the system prompt, add creative new function calls, you name it ...)


