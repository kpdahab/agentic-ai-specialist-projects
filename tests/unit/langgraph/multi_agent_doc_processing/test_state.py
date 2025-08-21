# =============================================================================
# Unit tests for state.py
# =============================================================================

from src.services.langgraph.multi_agent_doc_processing.state import DocumentState, DOCUMENT_TYPES
import pytest

def test_document_state_structure():
    """Ensure that a DocumentState object can be created correctly.""" 
    state = DocumentState(
        document_id="DOC-001",
        document_name="Sample Invoice",
        document_content="INVOICE #INV-2025-001\nAmount: $ 1000.00",
        document_type="invoice",
        confidence_score=0.0,
        extracted_data={},
        validation_results={},
        processing_stage="received",
        next_action="",
        error_count=0,
        human_review_required=False,
        processing_complete=False,
        messages=[],
    )

    assert state["document_id"] == "DOC-001"
    assert state["document_type"] == "invoice"
    assert isinstance(state["messages"], list)

@pytest.mark.unit
@pytest.mark.parametrize("doc_type", ["invoice", "contract", "receipt", "report"])
def test_document_types_configuration(doc_type):
    """Ensure each document type as the required keys"""
    config = DOCUMENT_TYPES[doc_type]

    assert "fields" in config
    assert "system" in config
    assert "threshold" in config
    assert isinstance(config["fields"], list)
    assert isinstance(config["system"], str)
