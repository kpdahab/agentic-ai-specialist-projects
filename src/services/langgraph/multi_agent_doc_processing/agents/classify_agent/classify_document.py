from src.services.langgraph.multi_agent_doc_processing.state import DocumentState, DOCUMENT_TYPES
from langchain_core.messages import AIMessage

def classify_document(state: DocumentState, llm) -> DocumentState:
    """
    Classifies the document type using an injected LLM.
    Returns updated state with 'document_type', 'confidence_score', etc.
    """
    content = state.get("document_content", "")
    detected_type = "unknown"
    confidence = 0.0

    prompt = f"""
Classify this document type. Return only one of: invoice, contract, receipt, or report.

Document:
{content}

Type:""".strip()

    try:
        response = llm.invoke(prompt)
        detected_type = ""
        if hasattr(response, "content"):
            detected_type = (response.content or "").strip().lower()
        else:
            detected_type = str(response).strip().lower()


        if detected_type in DOCUMENT_TYPES:
            confidence = 0.9
            state["next_action"] = "extract_data"
        else:
            # Fallback keyword-based classification
            content_lower = content.lower()
            if "invoice" in content_lower or "bill" in content_lower:
                detected_type, confidence = "invoice", 0.7
            elif "contract" in content_lower or "agreement" in content_lower:
                detected_type, confidence = "contract", 0.7
            elif "receipt" in content_lower:
                detected_type, confidence = "receipt", 0.7
            elif "report" in content_lower:
                detected_type, confidence = "report", 0.7
            else:
                detected_type, confidence = "unknown", 0.3

            if confidence < 0.8:
                state["human_review_required"] = True
                state["next_action"] = "human_review"
            else:
                state["next_action"] = "extract_data"

        state["document_type"] = detected_type
        state["confidence_score"] = confidence
        state["processing_stage"] = "classified"
        state.setdefault("messages", []).append(
            AIMessage(content=f"Classified as {detected_type}")
        )

    except Exception as e:
        state["error_count"] += 1
        state["next_action"] = "error_handling"
        state.setdefault("messages", []).append(
            AIMessage(content=f"Classification error: {e}")
        )

    return state

