from dotenv import load_dotenv
load_dotenv()

import argparse
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# --- Args ---
parser = argparse.ArgumentParser()
parser.add_argument("--session", default="default")
args = parser.parse_args()

# --- LLM ---
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    max_tokens=1024   # adjust as needed
)

# --- Prompt ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# --- Chain ---
chain = prompt | llm | StrOutputParser()

# --- SQLite-backed history ---
def get_history(session_id):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///chat_history.db"
    )

# --- Chain with history ---
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history"
)

# --- Chat loop ---
print(f"\nChatbot started (session: '{args.session}'). Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": args.session}}
    )
    print(f"Bot: {response}\n")