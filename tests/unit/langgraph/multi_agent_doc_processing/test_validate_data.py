import pytest
from src.services.langgraph.multi_agent_doc_processing.agents.validate_agent.validate_data import validate_data

@pytest.mark.unit
def test_validate_invoice_all_fields_good():
    test_state = {
       "document_id": "TEST-003",
       "document_name": "Invoice Good",
       "document_content": "",
       "document_type": "invoice",
       "extracted_data": {
           "invoice_number": "#12345",
           "date": "2024-06-01",
           "amount": "$ 1000.00",
           "vendor": "TechSupply Corp"
       },
       "confidence_score": 0,
       "validation_results": {},
       "processing_stage": "",
       "next_action": "",
       "error_count": 0,
       "human_review_required": False,
       "processing_complete": False,
       "messages": []
   }
    result_state = validate_data(test_state.copy())
    assert result_state["validation_results"]["overall_score"] == pytest.approx(1.00)
    assert result_state["next_action"] == "route_document"
    assert result_state["processing_stage"] == "validated"

@pytest.mark.unit
def test_validate_invoice_missing_fields():
   test_state = {
      # ...same fields...
      "document_type": "invoice",
      # Only partial extracted data (missing vendor and date)
      "extracted_data": {
          "invoice_number": "#12345",
          # missing date!
          # missing vendor!
          "amount": "$ 100"
      },
      # ...other fields...
      }
   result_state = validate_data(test_state.copy())
   assert result_state["validation_results"]["overall_score"] < .8     # Not all fields found/valid!
   assert set(result_state["validation_results"]["missing_fields"]) >= {"date", "vendor"}
