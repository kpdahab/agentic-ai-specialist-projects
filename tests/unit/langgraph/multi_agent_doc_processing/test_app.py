import json
import pytest
import app

@pytest.mark.unit
def test_handler_processes_document(monkeypatch):
    event = {"body": json.dumps({"document_content": "This is a test invoice for $ 500"})}
    context = {}

    # --- Fake workflow to return predictable results ---
    class FakeWorkflow:
        def invoke(self, state):
            return {
                "document_content": getattr(state, "document_content", ""),
                "document_type": "invoice",
                "processing_stage": "classified",
                "error_count": 0,
                "extracted_data": {"amount": "$ 500"}
            }

    # --- Monkeypatch app.get_app to return FakeWorkflow() ---
    monkeypatch.setattr(app, "get_app", lambda: FakeWorkflow())

    # --- Act ---
    response = app.handler(event, context)

    # --- Assert ---
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["document_type"] == "invoice"
    assert body["processing_stage"] == "classified"
    assert body["extracted_data"]["amount"] == "$ 500"
