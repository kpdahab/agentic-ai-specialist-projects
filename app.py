import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.services.langgraph.multi_agent_doc_processing.workflow import create_document_workflow
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState

# Load environment variables from .env file (for local dev)
load_dotenv()

# Retrieve API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not set. Please define it in your .env file or env vars.")

# Initialize LLM with API key
llm = ChatOpenAI(
    model="gpt-4o-mini",     # other options: gpt-4.1, gpt-3.5-turbo, etc.
    temperature=0,
    api_key=openai_api_key
)

# Build workflow once (re-used across requests)
app = create_document_workflow(llm=llm)

def handler(event, context):
    """
    AWS Lambda handler function.
    Triggered via API Gateway HTTP POST.
    """

    try:
        # API Gateway request wrapped in event["body"]
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        # Construct initial workflow state
        state = DocumentState(
            document_content=body.get("document_content", ""),
            human_review_required=body.get("human_review_required", False),
            error_count=body.get("error_count", 0),
            processing_stage="initial",
            messages=[]
        )

        # Run document workflow
        result = app.invoke(state)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
