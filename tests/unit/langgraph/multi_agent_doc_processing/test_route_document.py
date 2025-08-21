import pytest
from src.services.langgraph.multi_agent_doc_processing.agents.route_agent.route_document import route_document

@pytest.mark.unit
def test_route_invoice_autoapproved():
    test_state = {
       "document_id": "TEST-004",
       "document_name": "Invoice Good",
       "document_content": "",
       "document_type": "invoice",
       "extracted_data": {
           "invoice_number": "#12345",
           "date": "2024-06-01",
           "amount": "$ 1000.00",   # Below threshold (e.g., threshold=5000)
           "vendor": "TechSupply Corp"
       },
       "validation_results": {"overall_score": 1.0},
       "processing_stage": "",
       "next_action": "",
       "error_count": 0,
       "human_review_required": False,
       "processing_complete": False,
       "messages": []
   }
    result_state = route_document(test_state.copy())
    assert result_state["routing_result"]["target_system"] == "accounting_erp"
    assert not result_state["routing_result"]["requires_approval"]
    assert result_state["processing_stage"] == "routed"
    assert result_state["next_action"] == "complete"

@pytest.mark.unit
def test_route_invoice_requires_approval():
    test_state = {
      # ...same fields...
      "document_type": "invoice",
      # Amount above threshold for invoice (e.g., threshold=5000)
      "extracted_data": {
          # ...
          "amount": "$ 6000.00"
      },
      # Low validation score should also trigger approval requirement!
      "validation_results": {"overall_score": 0.7},
      # ...other fields...
      }
    result_state = route_document(test_state.copy())
    assert result_state["routing_result"]["requires_approval"]
    assert result_state["routing_result"]["routing_priority"] == "high"
