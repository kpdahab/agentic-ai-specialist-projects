import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, message_to_dict, messages_to_dict

from src.services.langgraph.multi_agent_doc_processing.workflow import create_document_workflow
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState

# Load .env locally (safe: in AWS Lambda with env vars set, this is a no-op)
load_dotenv()

# Global workflow reference
app = None


def get_app():
    """
    Initialize and return the LangGraph workflow.
    - In PROD (with OPENAI_API_KEY set): attaches OpenAI LLM.
    - In TEST/Local (no key): returns a dummy workflow (raises on invoke).
    """
    global app
    if app is not None:
        return app

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
        app = create_document_workflow(llm=llm)
    else:
        # No key → placeholder workflow
        class DummyWorkflow:
            def invoke(self, state):
                raise RuntimeError("OPENAI_API_KEY not set. Workflow not initialized.")
        app = DummyWorkflow()

    return app


import json
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, message_to_dict, messages_to_dict

def serialize(obj):
    """
    Recursive serializer for workflow outputs
    """
    # Handle Pydantic models (DocumentState, sub-models)
    if isinstance(obj, BaseModel):
        return {k: serialize(v) for k, v in obj.dict().items()}

    # Handle single LangChain message
    if isinstance(obj, BaseMessage):
        return message_to_dict(obj)

    # Handle list of LangChain messages
    if isinstance(obj, list):
        if all(isinstance(m, BaseMessage) for m in obj):
            return messages_to_dict(obj)
        return [serialize(v) for v in obj]

    # Handle dicts
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}

    # Pass through JSON-safe primitives
    return obj



def handler(event, context):
    try:
        workflow = get_app()

        # Handle API Gateway payloads (body may be str)
        body = json.loads(event["body"]) if "body" in event and isinstance(event["body"], str) else event

        # Build state object for workflow
        state = DocumentState(
            document_content=body.get("document_content", ""),
            document_type=body.get("document_type", "generic"), 
            human_review_required=body.get("human_review_required", False),
            error_count=body.get("error_count", 0),
            processing_stage="initial",
            messages=[],
        )


        # Run workflow
        result = workflow.invoke(state)

        # Serialize workflow output into JSON-safe dict
        safe_result = serialize(result)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(safe_result),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
