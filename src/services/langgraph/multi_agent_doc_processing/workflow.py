import functools
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama 
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState
from src.services.langgraph.multi_agent_doc_processing.agents.classify_agent.classify_document import classify_document
from src.services.langgraph.multi_agent_doc_processing.agents.extract_agent.extract_data import extract_data
from src.services.langgraph.multi_agent_doc_processing.agents.validate_agent.validate_data import validate_data
from src.services.langgraph.multi_agent_doc_processing.agents.route_agent.route_document import route_document

def create_document_workflow(llm=None) -> StateGraph:
    """
    Assemble the complete LangGraph document processing workflow.
    
    Returns:
        Compiled LangGraph workflow ready for invocation.
    """

    # Create the LLM instance
    if llm is None:
        llm = Ollama(model="llama3.2", temperature=0)
    
    # Create partial functions that "bake in" the llm argument
    classify_with_llm = functools.partial(classify_document, llm=llm)
    extract_with_llm = functools.partial(extract_data, llm=llm)

    workflow = StateGraph(DocumentState)

    # Register agent nodes (steps)
    workflow.add_node("classify", classify_with_llm)
    workflow.add_node("extract", extract_with_llm)
    workflow.add_node("validate", validate_data)
    workflow.add_node("route", route_document)

    # Set entry point and main edges
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "extract")
    workflow.add_edge("extract", "validate")

    # Conditional routing after validation step
    def should_route_or_review(state: DocumentState) -> str:
        return "human_review" if state.get('human_review_required', False) else "route"

    workflow.add_conditional_edges(
        "validate",
        should_route_or_review,
        {
            "route": "route",
            "human_review": END,
        }
    )

    # End after routing node completes
    workflow.add_edge("route", END)

    return workflow.compile()
