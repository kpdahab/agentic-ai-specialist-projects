# app.py
import os
import json
from dotenv import load_dotenv

from src.services.langgraph.multi_agent_doc_processing.workflow import create_document_workflow
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState

# For local dev, load variables from .env (safe to ignore if not present)
load_dotenv()

# Global workflow object (None if key missing)
app = None

def get_app():
    """
    Initialize and return the LangGraph workflow.
    - In PROD (with OPENAI_API_KEY set): attaches OpenAI LLM.
    - In TEST (no key): returns a dummy workflow placeholder (unit tests monkeypatch this).
    """
    global app
    if app is not None:
        return app

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        # Only import when needed, avoids crashing tests
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
        app = create_document_workflow(llm=llm)
    else:
        # No key found → placeholder (unit tests monkeypatch app.invoke)
        class DummyWorkflow:
            def invoke(self, state):
                raise RuntimeError("OPENAI_API_KEY not set. Workflow not initialized.")
        app = DummyWorkflow()

    return app


def handler(event, context):
    """
    AWS Lambda handler for API Gateway -> workflow integration.
    """
    try:
        workflow = get_app()

        # Parse request payload
        body = json.loads(event["body"]) if "body" in event else event

        state = DocumentState(
            document_content=body.get("document_content", ""),
            human_review_required=body.get("human_review_required", False),
            error_count=body.get("error_count", 0),
            processing_stage="initial",
            messages=[],
        )

        result = workflow.invoke(state)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
