from langgraph.prebuilt import create_react_agent
from ai.llms import get_openai_model
from ai.tools import document_tools


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


def get_agent():
    model = get_openai_model()

    return create_react_agent(
        model=model,
        tools=document_tools,
        state_modifier=SYSTEM_PROMPT,
    )
