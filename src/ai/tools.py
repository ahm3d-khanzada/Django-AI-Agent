from directories.models import Directory
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q



@tool
def list_documents(*, config: RunnableConfig, limit: int = 10):
    """
    List the most recent documents for the current user.

    Args:
        config (RunnableConfig): Configuration containing 'user_id'.
        limit (int): Maximum number of documents to return (default 10).

    Returns:
        dict: List of documents or an error message.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Validate limit
    # -----------------------------
    try:
        limit = int(limit)
        if limit <= 0:
            limit = 10
    except (ValueError, TypeError):
        limit = 10

    # -----------------------------
    # Query documents
    # -----------------------------
    try:
        queryset = Directory.objects.filter(owner_id=user_id, active=True).order_by("-created_at")[:limit]

        if not queryset.exists():
            return {"success": True, "documents": [], "message": "No documents found"}

        documents = [{"id": obj.id, "title": obj.title} for obj in queryset]

        return {"success": True, "documents": documents}

    except ValidationError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



@tool
def get_document(document_id: int, *, config: RunnableConfig):
    """
    Get a single document for the current user.

    Args:
        document_id (int): ID of the document to retrieve.
        config (RunnableConfig): Configuration containing 'user_id'.

    Returns:
        dict: Document info or error message.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Validate document_id
    # -----------------------------
    try:
        document_id = int(document_id)
    except (ValueError, TypeError):
        return {"error": "document_id must be an integer"}

    # -----------------------------
    # Fetch the document
    # -----------------------------
    try:
        obj = Directory.objects.get(id=document_id, owner_id=user_id, active=True)
        return {
            "success": True,
            "id": obj.id,
            "title": obj.title,
            "content": obj.content,
        }

    except Directory.DoesNotExist:
        return {"error": "Document not found"}

    except ValidationError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



@tool
def create_document(title: str, content: str, *, config: RunnableConfig):
    """
    Create a new document for the current user.

    Args:
        title (str): Title of the document (max 120 characters).
        content (str): Content of the document (long-form text).
        config (RunnableConfig): Configuration containing 'user_id'.

    Returns:
        dict: Created document info or error message.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Validate title and content
    # -----------------------------
    if not title or not title.strip():
        return {"error": "Title cannot be empty"}

    if len(title) > 120:
        title = title[:120]  # truncate to max 120 chars

    if not content or not content.strip():
        return {"error": "Content cannot be empty"}

    # -----------------------------
    # Create document safely
    # -----------------------------
    try:
        with transaction.atomic():
            obj = Directory.objects.create(
                title=title.strip(),
                content=content.strip(),
                owner_id=user_id,
                active=True
            )

            return {
                "success": True,
                "id": obj.id,
                "title": obj.title,
                "content": obj.content,
                "created_at": obj.created_at
            }

    except ValidationError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



@tool
def update_document(document_id: int, title: str = None, content: str = None, *, config: RunnableConfig):
    """
    Update a document's title and/or content for the current user.

    Args:
        document_id (int): ID of the document to update.
        title (str, optional): New title for the document.
        content (str, optional): New content for the document.
        config (RunnableConfig): Configuration containing 'user_id'.

    Returns:
        dict: Updated document info or error message.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Validate document_id
    # -----------------------------
    try:
        document_id = int(document_id)
    except (ValueError, TypeError):
        return {"error": "document_id must be an integer"}

    if not title and not content:
        return {"error": "At least one of 'title' or 'content' must be provided"}

    # -----------------------------
    # Update safely using transaction
    # -----------------------------
    try:
        with transaction.atomic():
            obj = Directory.objects.get(id=document_id, owner_id=user_id, active=True)

            if title:
                obj.title = title
            if content:
                obj.content = content

            obj.save()

            return {
                "success": True,
                "id": obj.id,
                "title": obj.title,
                "content": obj.content,
            }

    except Directory.DoesNotExist:
        return {"error": "Document not found"}

    except ValidationError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



@tool
def delete_document(document_id: int, *, config: RunnableConfig):
    """
    Delete a single document for the current user.

    Args:
        document_id (int): The ID of the document to delete.
        config (RunnableConfig): Configuration containing 'user_id'.

    Returns:
        dict: Success or error message.
    """

    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}


    try:
        document_id = int(document_id)
    except (ValueError, TypeError):
        return {"error": "document_id must be an integer"}

    try:
        with transaction.atomic():
            obj = Directory.objects.get(id=document_id, owner_id=user_id, active=True)
            obj.delete()
            return {"success": True, "message": f"Document {document_id} deleted successfully."}

    except Directory.DoesNotExist:
        return {"error": "Document not found"}

    except ValidationError as e:
        return {"error": str(e)}

    except Exception as e:
        # Catch unexpected errors
        return {"error": f"An unexpected error occurred: {str(e)}"}


@tool
def delete_all_documents(*, config: RunnableConfig):
    """
    Delete all documents for the current user.

    Args:
        config (RunnableConfig): Configuration containing 'user_id'.

    Returns:
        dict: Success message and number of deleted documents, or error.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Delete safely using transaction
    # -----------------------------
    try:
        with transaction.atomic():
            deleted_count, _ = Directory.objects.filter(owner_id=user_id, active=True).delete()
            
            if deleted_count == 0:
                return {"success": True, "deleted_count": 0, "message": "No documents to delete"}
            
            return {"success": True, "deleted_count": deleted_count, "message": "All documents deleted successfully"}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
    


@tool
def search_query_documents(query: str, *, config: RunnableConfig, limit: int = 10):
    """
    Search documents for the current user by a query string in title or content.

    Args:
        query (str): The search query.
        config (RunnableConfig): Configuration containing 'user_id'.
        limit (int): Maximum number of results to return (default 10).

    Returns:
        dict: List of matched documents or an error message.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")

    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    lookups = {
        "owner_id": user_id,
        "active": True,
    }

    # -----------------------------
    # Validate query
    # -----------------------------
    if not query or not query.strip():
        return {"error": "Search query cannot be empty"}

    query = query.strip()

    # -----------------------------
    # Validate limit
    # -----------------------------
    try:
        limit = int(limit)
        if limit <= 0:
            limit = 10
    except (ValueError, TypeError):
        limit = 10

    # -----------------------------
    # Perform search using lookups
    # -----------------------------
    try:
        queryset = Directory.objects.filter(**lookups).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")[:limit]

        if not queryset.exists():
            return {"success": True, "documents": [], "message": "No documents matched your query"}

        documents = [{"id": obj.id, "title": obj.title, "content": obj.content} for obj in queryset]

        return {"success": True, "documents": documents}

    except ValidationError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



# -----------------------------
# TOOL LIST
# -----------------------------
document_tools = [
    list_documents,
    get_document,
    create_document,
    update_document,
    delete_document,
    delete_all_documents,
    search_query_documents,
]
