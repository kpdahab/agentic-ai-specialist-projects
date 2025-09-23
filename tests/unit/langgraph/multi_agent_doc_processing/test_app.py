import json
import pytest
import app   # thanks to conftest.py, this is always your root app.py


# -------------------------------
# get_openai_key() Tests
# -------------------------------

@pytest.mark.unit
def test_get_openai_key_from_env(monkeypatch):
    """Ensure OPENAI_API_KEY in env is used."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
    monkeypatch.delenv("OPENAI_SECRET_ARN", raising=False)
    assert app.get_openai_key() == "test-key-123"


@pytest.mark.unit
def test_get_openai_key_from_secrets_manager(monkeypatch):
    """Ensure fallback to Secrets Manager ARN works with boto3 mock."""

    class FakeSecretsManager:
        def get_secret_value(self, SecretId):
            assert SecretId == "fake-arn"
            return {"SecretString": "secret-from-aws"}

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_SECRET_ARN", "fake-arn")

    fake_boto3 = type(
        "FakeBoto3",
        (),
        {"client": staticmethod(lambda svc: FakeSecretsManager())}
    )
    monkeypatch.setattr(app, "boto3", fake_boto3)

    assert app.get_openai_key() == "secret-from-aws"


# -------------------------------
# handler() Tests
# -------------------------------

@pytest.mark.unit
def test_handler_processes_document(monkeypatch):
    event = {"body": json.dumps({"document_content": "Invoice for $ 500"})}
    context = {}

    class FakeWorkflow:
        def invoke(self, state):
            return {
                "document_content": state.document_content,
                "document_type": "invoice",
                "processing_stage": "classified",
                "error_count": 0,
                "extracted_data": {"amount": "$ 500"},
            }

    class FakeState:
        def __init__(self, document_content, **kwargs):
            self.document_content = document_content

    monkeypatch.setattr("app.get_app", lambda: FakeWorkflow())
    monkeypatch.setattr(app, "DocumentState", FakeState)

    response = app.handler(event, context)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["document_type"] == "invoice"
    assert body["extracted_data"]["amount"] == "$ 500"



@pytest.mark.unit
def test_handler_handles_exception(monkeypatch):
    """Handler should return 500 on workflow failure."""
    event = {"body": json.dumps({"document_content": "bad input"})}
    context = {}

    class BadWorkflow:
        def invoke(self, state):
            raise RuntimeError("workflow failed")

    monkeypatch.setattr("app.get_app", lambda: BadWorkflow())

    response = app.handler(event, context)
    body = json.loads(response["body"])
    assert response["statusCode"] == 500
    assert "workflow failed" in body["error"]
