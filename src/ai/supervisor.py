from langgraph_supervisor import create_supervisor
from ai.llms import get_openai_model
from ai import agents

# Step 1: Supervisor
def get_supervisor(model=None, checkpointer=None):
    llm_model = get_openai_model(model=model)

    supervisor = create_supervisor(
        agents=[
            agents.get_document_agent(llm_model, checkpointer),
            agents.get_movie_agent(llm_model, checkpointer),
        ],
        model=llm_model,
        prompt=(
            "You manage the document management assistant and a "
            "movie discovery assistant. Delegate user requests to the "
            "appropriate agent based on the user's needs. "
            "If a request requires multiple steps or both agents, handle one step at a time, "
            "delegating to one agent, then using its output to delegate to the other if needed. "
            "For example, if the user wants to search for a movie and create a document from the results, "
            "first delegate the search to the movie agent, then delegate document creation to the document agent."
        ),
    ).compile(checkpointer=checkpointer)

    return supervisor