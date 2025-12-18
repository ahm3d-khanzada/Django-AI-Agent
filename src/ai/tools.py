from directories.models  import Directory
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

@tool
def list_documents(config: RunnableConfig):

    """
    Get a document for a current user
    """
    print(config)
    metadata = config.get("metadata") or config.get("configurable")
    user_id = metadata.get("user_id") 
    query_set = Directory.objects.filter(owner_id = user_id , active=True)
    response_data = []
    for obj in query_set:
        response_data.append({
            "id": obj.id,
            "title": obj.title,
        })

    return response_data

@tool
def get_document(document_id: int, config: RunnableConfig):
    """
    Get a document for the current user
    """
    print(config)

    # Extract user_id from config
    metadata = config.get("metadata") or config.get("configurable")
    user_id = metadata.get("user_id") if metadata else None

    if not user_id:
        raise Exception("Invalid request: user_id missing in config")

    try:
        # Fetch the document for this user and only active
        obj = Directory.objects.get(id=document_id, owner_id=user_id, active=True)

        # Prepare response
        response_data = {
            "id": obj.id,
            "title": obj.title,
            "content": obj.content,
        }
        return response_data

    except Directory.DoesNotExist:
        # Document not found for this user
        return None

    except Exception as e:
        # Any other error
        raise Exception(f"Invalid request for document details: {str(e)}")
