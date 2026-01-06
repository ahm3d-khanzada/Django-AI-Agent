from langchain.agents import create_agent
from ai.tools.documents import document_tools
from ai.tools.movie_discovery import movie_tools


SYSTEM_PROMPT = """
You are an AI assistant connected to a document management system.

Rules:
- Always call tools when needed
- NEVER show raw tool output like [] or JSON
- Convert tool responses into natural language
- If list_documents returns empty, reply:
  "You have no recent documents."
- Be concise and user-friendly
"""


def get_document_agent(llm, checkpointer=None):
    return create_agent(
        model=llm,
        tools=document_tools,      # ✅ flat list
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
        name="document_agent",
    )


def get_movie_agent(llm, checkpointer=None):
    return create_agent(
        model=llm,
        tools=movie_tools,         # ✅ flat list
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
        name="movie_agent",
    )
