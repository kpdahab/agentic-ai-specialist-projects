import re
from langchain_core.messages import AIMessage
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState, DOCUMENT_TYPES

def validate_data(state: DocumentState) -> DocumentState:
    """Validate extracted data quality for the given document."""
    doc_type = state['document_type']
    extracted_data = state['extracted_data']
    required_fields = DOCUMENT_TYPES.get(doc_type, {}).get('fields', [])

    print(f"Validating {doc_type} data quality...")

    validation_results = {
        'overall_score': 0.0,
        'field_scores': {},
        'missing_fields': [],
        'issues': []
    }

    try:
        field_scores = []

        for field in required_fields:
            value = extracted_data.get(field, 'NOT_FOUND')

            if value == 'NOT_FOUND' or not value.strip():
                validation_results['missing_fields'].append(field)
                field_score = 0.0
                print(f"   Missing: {field}")
            else:
                # Field-specific validation
                if field in ['amount', 'value']:
                    field_score = 1.0 if validate_amount(value) else 0.3
                elif field in ['date', 'effective_date']:
                    field_score = 1.0 if validate_date(value) else 0.4
                elif field in ['invoice_number', 'contract_number']:
                    field_score = 1.0 if len(value) >= 3 else 0.5
                else:
                    field_score = 1.0 if 2 <= len(value) <= 200 else 0.6

                status = "High" if field_score >= 0.8 else "Moderate"
                print(f"   {status} confidence: {field}: {value} (score: {field_score:.1f})")

            validation_results['field_scores'][field] = field_score
            field_scores.append(field_score)

        overall_score = sum(field_scores) / len(field_scores) if field_scores else 0.0
        validation_results['overall_score'] = overall_score

        state['validation_results'] = validation_results
        state['processing_stage'] = 'validated'

        # Determine next action
        if overall_score >= 0.8:
            state['next_action'] = 'route_document'
            print(f"High quality ({overall_score:.1%}) → Routing")
        elif overall_score >= 0.6:
            state['next_action'] = 'route_document'
            print(f"Moderate quality ({overall_score:.1%}) → Routing with caution")
        else:
            state['human_review_required'] = True
            state['next_action'] = 'human_review'
            print(f"Low quality ({overall_score:.1%}) → Human review")

        state.setdefault('messages', []).append(AIMessage(content=f"Validation: {overall_score:.1%} quality"))

    except Exception as e:
        print(f"Validation error: {e}")
        state['error_count'] += 1
        state['next_action'] = 'error_handling'

    return state

def validate_amount(amount_str: str) -> bool:
    """Validate monetary amount."""
    try:
        cleaned = re.sub(r'[$,]', '', amount_str.strip())
        amount = float(cleaned)
        return 0.01 <= amount <= 1000000
    except Exception:
        return False

def validate_date(date_str: str) -> bool:
    """Validate date format."""
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4}',
        r'\d{1,2}-\d{1,2}-\d{2,4}',
        r'\d{4}-\d{1,2}-\d{1,2}',
        r'\w+ \d{1,2}, \d{4}'
    ]
    return any(re.match(pattern, date_str.strip()) for pattern in patterns)
