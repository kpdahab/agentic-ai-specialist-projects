import re
import time
from datetime import datetime
from langchain_core.messages import AIMessage
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState, DOCUMENT_TYPES

def route_document(state: DocumentState) -> DocumentState:
    """Route validated documents to appropriate business systems."""
    doc_type = state['document_type']
    validation_score = state.get('validation_results', {}).get('overall_score', 0)
    extracted_data = state.get('extracted_data', {})

    print(f"Routing {doc_type} to business systems...")

    try:
        config = DOCUMENT_TYPES.get(doc_type, {})
        target_system = config.get('system', 'manual_review')
        threshold = config.get('threshold', 0)

        requires_approval = False

        # Approval logic based on validation score and thresholds
        if validation_score < 0.8:
            requires_approval = True

        if doc_type in ['invoice', 'contract'] and 'amount' in extracted_data:
            try:
                amount_str = extracted_data['amount']
                amount = float(re.sub(r'[$,]', '', amount_str))
                if amount > threshold:
                    requires_approval = True
            except Exception:
                requires_approval = True  # Default to approval if parsing fails

        if doc_type == 'contract':
            requires_approval = True

        routing_result = {
            'target_system': target_system,
            'requires_approval': requires_approval,
            'routing_priority': 'high' if requires_approval else 'medium',
            'reference_id': f"REF-{doc_type.upper()}-{int(time.time()) % 10000:04d}",
            'routing_timestamp': datetime.now().isoformat(),
            'integration_status': 'success'
        }

        state['routing_result'] = routing_result
        state['processing_stage'] = 'routed'
        state['processing_complete'] = True
        state['next_action'] = 'complete'

        print(f"   Target: {target_system}")
        print(f"   Priority: {routing_result['routing_priority']}")
        print(f"   Approval: {'Required' if requires_approval else 'Auto-approved'}")
        print(f"   Reference: {routing_result['reference_id']}")

        state.setdefault('messages', []).append(
            AIMessage(content=f"Routed to {target_system} - {routing_result['reference_id']}")
        )

    except Exception as e:
        print(f"Routing error: {e}")
        state['error_count'] += 1
        state['next_action'] = 'error_handling'

    return state
