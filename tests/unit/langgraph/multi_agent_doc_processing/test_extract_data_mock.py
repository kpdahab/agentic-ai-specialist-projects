import pytest
import json
from src.services.langgraph.multi_agent_doc_processing.agents.extract_agent.extract_data import extract_data

class MockLLMResponse:
    def __init__(self, content):
        self.content = content

class MockLLM:
    def __init__(self, content):
        self._content = content

    def invoke(self, prompt):
        return MockLLMResponse(self._content)

@pytest.mark.unit
def test_extract_invoice_fields_with_mock_llm():
    mock_json_response = json.dumps({
       "invoice_number": "#12345",
       "date": "2024-06-01",
       "amount": "$ 1000.00",
       "vendor": "TechSupply Corp"
    })
    llm = MockLLM(mock_json_response)

    state = {
       'document_id': 'TEST-002',
       'document_name': 'Invoice Sample',
       'document_content': 'INVOICE #12345\nDate: 2024-06-01\nVendor: TechSupply Corp\nAmount Due: $ 1000.00',
       'document_type': 'invoice',
       'confidence_score': 0.0,
       'extracted_data': {},
       'validation_results': {},
       'processing_stage': '',
       'next_action': '',
       'error_count': 0,
       'human_review_required': False,
       'processing_complete': False,
       'messages': []
   }
    result_state = extract_data(state.copy(), llm=llm)
    assert result_state["extracted_data"]["invoice_number"] == "#12345"
    assert result_state["extracted_data"]["amount"] == "$ 1000.00"
    assert result_state["processing_stage"] == "extracted"
    assert result_state["next_action"] == "validate_data"

@pytest.mark.unit
def test_extract_missing_fields_with_mock_llm():
    # Simulate a model that returns incomplete JSON or nothing at all.
    llm_response_content = "{}"
    llm = MockLLM(llm_response_content)

    state = {
      # ...same as above...
      "document_content": "",
      "document_type": "invoice",
      # ...
      }
      
    result_state = extract_data(state.copy(), llm=llm)
    for field in ["invoice_number", "date", "amount", "vendor"]:
         assert result_state["extracted_data"][field] == "NOT_FOUND"
