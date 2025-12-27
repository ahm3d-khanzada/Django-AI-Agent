from langchain_openai import ChatOpenAI
from django.conf import settings


def get_openai_model(model="gpt-4o-mini"):
    return ChatOpenAI(
        model=model,
        temperature=0,
        max_retries=3,
        api_key=settings.OPENAI_API_KEY,
    )
