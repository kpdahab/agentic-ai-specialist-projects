# =============================================================================
""" 
state.py
Defines the shared state schema (`Document State`) and document type configurations
for the LangGraph Document Processing Pipeline Project. 
"""
# =============================================================================

from typing_extensions import TypedDict
from typing import Dict, Any, List 

class DocumentState(TypedDict):

    # Document metadata
    document_id: str
    document_name: str
    document_content: str
    document_type: str

    # Processing results
    confidence_score: float
    extracted_data: Dict[str, Any]
    validation_results: Dict[str, Any]

    # Workflow control/status flags
    processing_stage: str
    next_action: str
    error_count: int
    human_review_required: bool
    processing_complete: bool

    # Message log for Ai-humnan conversation, debugging, or audit trail
    messages: List[Any]

DOCUMENT_TYPES: Dict[str, Dict[str, Any]] = {
    "invoice": {
        "fields": ["invoice_number", "date", "amount", "vendor"],
        "system": "accounting_erp",
        "threshold": 5000,
    },
    "contract": {
        "fields": ["contract_number", "parties", "effective_date", "value"],
        "system": "legal_management",
        "threshold": 0,
    },
    "receipt": {
        "fields": ["date", "amount", "vendor"],
        "system": "expense_management",
        "threshold": 500,
    },
    "report": {
        "fields": ["title", "date", "author"],
        "system": "document_repository",
        "threshold": float("inf"),
    },
}