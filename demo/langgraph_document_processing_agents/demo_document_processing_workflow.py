# =============================================================================
# Demo script: end-to-end workflow processing with Ollama as the LLM.
# =============================================================================

import requests, sys
from src.services.langgraph.multi_agent_doc_processing.workflow import create_document_workflow
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState
from langchain_ollama import OllamaLLM

print("🧪 END-TO-END WORKFLOW DEMO (using Ollama)")
print("=" * 55)

try:
    requests.get("http://localhost:11434/api/version", timeout=2)
except Exception:
    sys.exit("❌ Ollama server not running. Start it first with `brew services start ollama` or `ollama serve`.")


# Use Ollama as the backend LLM (adjust model as needed)
llm = OllamaLLM(model="llama3.2", temperature=0)

workflow = create_document_workflow(llm=llm)

# Example documents for demo
test_documents = [
    ("Invoice", """
        INVOICE #INV-2025-045
        Date: January 15, 2025
        Vendor: Enterprise Tech Solutions
        Amount: $ 12,500.00
    """),
    ("Contract", """
        SOFTWARE LICENSE AGREEMENT
        Contract Number: SLA-2025-012
        Parties: DocuFlow Inc. & CloudTech Corp
    """),
    ("Report", """
        Q1 2025 PERFORMANCE REPORT
        Title: AI Implementation Progress
        Summary: Automated 90% of document processing with 99% time reduction.
    """),
]

for idx, (name, content) in enumerate(test_documents, 1):
    print(f"\n📄 {idx}. {name}")
    print("-" * 45)

    state = DocumentState(
        document_id=f"DEMO-{idx:03d}",
        document_name=name,
        document_content=content.strip(),
        human_review_required=False,
        error_count=0,
        processing_stage="received",
        messages=[]
    )

    try:
        result = workflow.invoke(state)
        print(f"   📋 Type: {result.get('document_type', 'unknown')}")
        print(f"   🎯 Confidence: {result.get('confidence_score', 0):.0%}")
        print(f"   🏁 Stage: {result.get('processing_stage')}")
        print(f"   👀 Needs Review? {'Yes' if result.get('human_review_required') else 'No'}")

    except Exception as e:
        print(f"   ❌ Error while processing {name}: {e}")
