import functools
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState
from src.services.langgraph.multi_agent_doc_processing.agents.classify_agent.classify_document import classify_document
from src.services.langgraph.multi_agent_doc_processing.agents.extract_agent.extract_data import extract_data
from src.services.langgraph.multi_agent_doc_processing.agents.validate_agent.validate_data import validate_data
from src.services.langgraph.multi_agent_doc_processing.agents.route_agent.route_document import route_document

def create_document_workflow(llm=None) -> StateGraph:
    """
    Assemble the complete LangGraph document processing workflow.
    Allows injection of a mock llm for testing.
    """
    # Use injected LLM if provided, else create real one
    if llm is None:
        llm = OllamaLLM(model="llama3.2", temperature=0)

    classify_with_llm = functools.partial(classify_document, llm=llm)
    extract_with_llm = functools.partial(extract_data, llm=llm)

    workflow = StateGraph(DocumentState)
    workflow.add_node("classify", classify_with_llm)
    workflow.add_node("extract", extract_with_llm)
    workflow.add_node("validate", validate_data)
    workflow.add_node("route", route_document)

    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "extract")
    workflow.add_edge("extract", "validate")

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
    workflow.add_edge("route", END)
    return workflow.compile()
