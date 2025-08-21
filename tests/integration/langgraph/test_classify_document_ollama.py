import pytest
from src.services.langgraph.agents.classify_agent.classify_document import classify_document
from src.llm_manager import get_llm

@pytest.mark.integration  # Mark as integration since it requires Ollama running locally
@pytest.mark.parametrize(
    "content,expected",
    [
        ("INVOICE #123 for payment", "invoice"),
        ("This is a contract agreement.", "contract"),
        ("Attached is your receipt from purchase.", "receipt"),
        ("Quarterly performance report Q1.", "report"),
        ("Random text with no keywords.", "unknown"),  # Fallback triggers here!
    ]
)
def test_classify_document_with_ollama(content, expected):
    try:
        llm = get_llm(provider="ollama")
    except Exception as e:
        pytest.skip(f"Ollama not available: {e}")

    state = {
        'document_id': 'TEST-001',
        'document_name': 'Test Doc',
        'document_content': content,
        'processing_stage': '',
        'confidence_score': 0.0,
        'error_count': 0,
        'extracted_data': {},
        'validation_results': {},
        'next_action': '',
        'human_review_required': False,
        'processing_complete': False,
        'messages': [],
        'document_type': ''
    }
    result_state = classify_document(state.copy(), llm=llm)
    assert result_state['document_type'] == expected
 