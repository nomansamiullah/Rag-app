import uuid
from datetime import datetime
from typing import Dict, Any

def generate_doc_id() -> str:
    """Generate unique document ID"""
    return str(uuid.uuid4())

def generate_conversation_id() -> str:
    """Generate unique conversation ID"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def add_timestamp_to_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Add timestamp to metadata"""
    if metadata is None:
        metadata = {}
    
    metadata.update({
        'timestamp': get_current_timestamp()
    })
    
    return metadata

def validate_openai_api_key(api_key: str) -> bool:
    """Basic validation for OpenAI API key format"""
    return api_key and isinstance(api_key, str) and api_key.startswith('sk-')