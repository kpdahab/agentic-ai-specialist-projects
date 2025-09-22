import json
import pytest
import app

@pytest.mark.unit
def test_handler_processes_document(monkeypatch):
    event = {"body": json.dumps({"document_content": "This is a test invoice for $ 500"})}
    context = {}

    # Patch invoke method of real app to always return a fake result
    monkeypatch.setattr(app.app, "invoke", lambda state: {
        "document_content": getattr(state, "document_content", ""),
        "document_type": "invoice",
        "processing_stage": "classified",
        "error_count": 0,
        "extracted_data": {"amount": "$ 500"}
    })

    response = app.handler(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["document_type"] == "invoice"
    assert body["processing_stage"] == "classified"
    assert body["extracted_data"]["amount"] == "$ 500"
