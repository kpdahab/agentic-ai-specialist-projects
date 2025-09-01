import json
from langchain_core.messages import AIMessage
from src.services.langgraph.multi_agent_doc_processing.state import DocumentState, DOCUMENT_TYPES

def extract_data(state: DocumentState, llm) -> DocumentState:
    """Extract structured data based on document type using an injected LLM."""
    doc_type = state['document_type']
    required_fields = DOCUMENT_TYPES.get(doc_type, {}).get('fields', [])
    
    print(f"Extracting {len(required_fields)} fields from {doc_type}")
    
    prompt = f"""
    Extract these fields from the {doc_type}:
    {', '.join(required_fields)}

    Document:
    {state['document_content']}

    Return JSON format. Use "NOT_FOUND" for missing fields:
    {{
        {', '.join([f'"{field}": "value"' for field in required_fields])}
    }}
    """.strip()
    
    try:
        # Handle both new and old LLM outputs
        response = llm.invoke(prompt)
        if hasattr(response, "content"):   # old community Ollama
            raw_output = response.content
        else:                              # new langchain-ollama
            raw_output = str(response)

        # Try to extract JSON
        json_start = raw_output.find('{')
        json_end = raw_output.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = raw_output[json_start:json_end]
            try:
                extracted_data = json.loads(json_str)
            except json.JSONDecodeError:
                print("⚠️ LLM returned malformed JSON, marking all fields as NOT_FOUND")
                extracted_data = {field: "NOT_FOUND" for field in required_fields}
        else:
            extracted_data = {field: "NOT_FOUND" for field in required_fields}
        
        # Ensure all required fields exist
        for field in required_fields:
            if field not in extracted_data:
                extracted_data[field] = "NOT_FOUND"
        
        state['extracted_data'] = extracted_data
        state['processing_stage'] = 'extracted'
        state['next_action'] = 'validate_data'

        # Logging
        found_count = len([v for v in extracted_data.values() if v != "NOT_FOUND"])
        print(f"Extracted {found_count}/{len(required_fields)} fields")
        
        for field, value in extracted_data.items():
            status = "Found" if value != "NOT_FOUND" else "Missing"
            print(f"   {status}: {field}: {value}")
        
        state.setdefault('messages', []).append(
            AIMessage(content=f"Extracted {found_count} fields")
        )
        
    except Exception as e:
        print(f"Extraction error: {e}")
        state['error_count'] += 1
        state['next_action'] = 'error_handling'
    
    return state
