# MultiTurnCli

A small terminal chatbot that uses Groq through LangChain and stores conversation history in SQLite.

## Project overview

MultiTurnCli is a command-line chatbot built in Python. It connects to Groq's hosted LLM API through LangChain and keeps track of previous messages so the assistant can respond with context during a multi-turn conversation.

The project is intentionally lightweight: it runs from a single `chat.py` script, reads secrets from a local `.env` file, and stores chat history in a local SQLite database. This makes it easy to run locally, test different sessions, and package with Docker.

## Features

- Interactive terminal chat loop
- Groq LLM integration using `langchain-groq`
- Conversation memory backed by SQLite
- Named sessions with the `--session` argument
- Environment-based API key configuration
- Docker support for reproducible runs

## How it works

When you start the app, `chat.py` loads environment variables from `.env`, creates a Groq chat model, and builds a LangChain prompt that includes the current user message plus previous conversation history.

Conversation memory is handled by `SQLChatMessageHistory`, which stores messages in `chat_history.db`. The `--session` option lets you keep separate conversations in the same database. For example, `--session study-notes` and `--session coding-help` will maintain different histories.

## Project structure

```text
.
├── chat.py           # Main CLI chatbot application
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker image definition
├── .dockerignore     # Files excluded from Docker builds
├── .env.example      # Example environment variables
└── README.md         # Project documentation
```

## Local setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Groq API key to `.env`, then run:

```bash
python chat.py
```

To end the chat, type `exit` or `quit` and press Enter.

Use a named chat session with:

```bash
python chat.py --session my-session
```

## Docker

Build the image:

```bash
docker build -t multiturncli .
```

Run it interactively with your local `.env` file:

```bash
docker run --rm -it --env-file .env multiturncli
```

Use a named session in Docker:

```bash
docker run --rm -it --env-file .env multiturncli python chat.py --session my-session
```
