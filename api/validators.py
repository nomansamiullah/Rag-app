from typing import Dict, Any, List, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_add_document(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate add document request"""
    if not data:
        raise ValidationError("Request body is required")
    
    if 'text' not in data:
        raise ValidationError("Text content is required")
    
    if not isinstance(data['text'], str) or not data['text'].strip():
        raise ValidationError("Text must be a non-empty string")
    
    metadata = data.get('metadata', {})
    if metadata and not isinstance(metadata, dict):
        raise ValidationError("Metadata must be a dictionary")
    
    return {
        'text': data['text'].strip(),
        'metadata': metadata
    }

def validate_add_documents(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate add documents batch request"""
    if not data:
        raise ValidationError("Request body is required")
    
    if 'documents' not in data:
        raise ValidationError("Documents array is required")
    
    documents = data['documents']
    if not isinstance(documents, list):
        raise ValidationError("Documents must be an array")
    
    if not documents:
        raise ValidationError("Documents array cannot be empty")
    
    # Validate each document
    validated_documents = []
    for i, doc in enumerate(documents):
        if not isinstance(doc, str) or not doc.strip():
            raise ValidationError(f"Document at index {i} must be a non-empty string")
        validated_documents.append(doc.strip())
    
    # Validate metadatas if provided
    metadatas = data.get('metadatas', None)
    if metadatas is not None:
        if not isinstance(metadatas, list):
            raise ValidationError("Metadatas must be an array")
        
        if len(metadatas) != len(documents):
            raise ValidationError("Metadatas array length must match documents array length")
        
        for i, metadata in enumerate(metadatas):
            if not isinstance(metadata, dict):
                raise ValidationError(f"Metadata at index {i} must be a dictionary")
    
    return {
        'documents': validated_documents,
        'metadatas': metadatas
    }

def validate_chat_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate chat request"""
    if not data:
        raise ValidationError("Request body is required")
    
    if 'query' not in data:
        raise ValidationError("Query is required")
    
    query = data['query']
    if not isinstance(query, str) or not query.strip():
        raise ValidationError("Query must be a non-empty string")
    
    conversation_id = data.get('conversation_id', None)
    if conversation_id and not isinstance(conversation_id, str):
        raise ValidationError("Conversation ID must be a string")
    
    n_results = data.get('n_results', 5)
    if not isinstance(n_results, int) or n_results < 1 or n_results > 20:
        raise ValidationError("n_results must be an integer between 1 and 20")
    
    return {
        'query': query.strip(),
        'conversation_id': conversation_id,
        'n_results': n_results
    }

def validate_retrieve_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate retrieve documents request"""
    if not data:
        raise ValidationError("Request body is required")
    
    if 'query' not in data:
        raise ValidationError("Query is required")
    
    query = data['query']
    if not isinstance(query, str) or not query.strip():
        raise ValidationError("Query must be a non-empty string")
    
    n_results = data.get('n_results', 5)
    if not isinstance(n_results, int) or n_results < 1 or n_results > 20:
        raise ValidationError("n_results must be an integer between 1 and 20")
    
    return {
        'query': query.strip(),
        'n_results': n_results
    }