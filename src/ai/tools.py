from directories.models import Directory
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def list_documents(*, config: RunnableConfig):
    """List recent documents for the current user"""

    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        raise ValueError("user_id missing in config")

    queryset = (
        Directory.objects
        .filter(owner_id=int(user_id), active=True)
        .order_by("-created_at")[:5]
    )

    return [
        {
            "id": obj.id,
            "title": obj.title,
        }
        for obj in queryset
    ]


@tool
def get_document(document_id: int, *, config: RunnableConfig):
    """Get a single document for the current user"""

    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        raise ValueError("user_id missing in config")

    try:
        obj = Directory.objects.get(
            id=document_id,
            owner_id=int(user_id),
            active=True,
        )

        return {
            "id": obj.id,
            "title": obj.title,
            "content": obj.content,
        }

    except Directory.DoesNotExist:
        return {"error": "Document not found"}


document_tools = [list_documents, get_document]
