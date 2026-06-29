# MultiTurnCli

A small terminal chatbot that uses Groq through LangChain and stores conversation history in SQLite.

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
