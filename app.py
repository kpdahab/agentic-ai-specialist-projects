import boto3, os, json
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, message_to_dict, messages_to_dict

from src.services.langgraph.multi_agent_doc_processing.workflow import create_document_workflow
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState

# Load .env locally (safe: in AWS Lambda with env vars set, this is a no-op)
load_dotenv()

# Global workflow reference
workflow_instance = None

def get_openai_key():
    """
    Retrieve OpenAI API Key.
    - Local dev: from OPENAI_API_KEY in env/.env
    - AWS Lambda: from AWS Secrets Manager via OPENAI_SECRET_ARN
    """
    if os.getenv("OPENAI_API_KEY"):
        return os.getenv("OPENAI_API_KEY")

    secret_arn = os.getenv("OPENAI_SECRET_ARN")
    if secret_arn:
        sm = boto3.client("secretsmanager")
        val = sm.get_secret_value(SecretId=secret_arn)
        return val["SecretString"]

    raise RuntimeError("No OpenAI API Key available (checked OPENAI_API_KEY and OPENAI_SECRET_ARN)")



def get_app():
    """
    Initialize and return the LangGraph workflow.
    """
    global workflow_instance
    if workflow_instance is not None:
        return workflow_instance

    try:
        api_key = get_openai_key()
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
        workflow_instance = create_document_workflow(llm=llm)
    except Exception:
        class DummyWorkflow:
            def invoke(self, state):
                raise RuntimeError("OPENAI_API_KEY not set. Workflow not initialized.")
        workflow_instance = DummyWorkflow()

    return workflow_instance


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
