import pytest
from src.services.langgraph.multi_agent_doc_processing.workflow import create_document_workflow
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState

class MockLLMResponse:
    def __init__(self, content): self.content = content
class MockLLM:
    def invoke(self, prompt):
        if "Classify" in prompt:
            return MockLLMResponse("invoice")
        if "Extract" in prompt:
            return MockLLMResponse('{"invoice_number": "#123", "amount": "$ 1000"}')
        return MockLLMResponse("ok")

@pytest.mark.integration
def test_document_processing_workflow_end_to_end():
    mock_llm = MockLLM()
    workflow = create_document_workflow(llm=mock_llm)

    doc = DocumentState(
        document_id="TEST-001",
        document_name="Invoice Example",
        document_content="This is a fake invoice for $ 1000.",
        human_review_required=False,
        error_count=0,
        processing_stage="received",
        messages=[]
    )

    result = workflow.invoke(doc)
    assert result["document_type"] == "invoice"
    assert result["processing_stage"] != "received"
    assert "extracted_data" in result
