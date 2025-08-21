import pytest
from src.services.langgraph.multi_agent_doc_processing.agents.classify_agent.classify_document import classify_document

# Minimal mock class that mimics the real LLM's .invoke() method
class MockLLMResponse:
    def __init__(self, content):
        self.content = content

class MockLLM:
    def __init__(self, response_content):
        self.response_content = response_content

    def invoke(self, prompt):
        return MockLLMResponse(self.response_content)

@pytest.mark.unit
@pytest.mark.parametrize(
    "content,llm_response,expected_type",
    [
        ("INVOICE #123 for payment",     "invoice",   "invoice"),
        ("This is a contract agreement","contract",   "contract"),
        ("Attached is your receipt.",   "receipt",   "receipt"),
        ("Quarterly performance report","report",     "report"),
        ("Random unrelated text.",      "",           "unknown"), # fallback triggers here!
    ]
)
def test_classify_document_with_mock_llm(content, llm_response, expected_type):
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

    llm = MockLLM(llm_response)
    result_state = classify_document(state.copy(), llm)
    assert result_state['document_type'] == expected_type
