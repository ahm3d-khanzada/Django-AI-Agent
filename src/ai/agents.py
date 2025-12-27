from langgraph.prebuilt import create_react_agent
from ai.llms import get_openai_model
from ai.tools import document_tools
from langchain.agents import create_agent


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


def get_agent(
    model: str = "gpt-4o-mini",
    checkpointer=None,
):
    llm = get_openai_model(model=model)

    return create_agent(
        model=llm,
        tools=document_tools,
        # prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
