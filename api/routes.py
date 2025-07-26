from flask import Blueprint, request, jsonify
from datetime import datetime
from models.rag_chatbot import RAGChatbot
from api.validators import (
    validate_add_document,
    validate_add_documents,
    validate_chat_request,
    validate_retrieve_request,
    ValidationError
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize chatbot
chatbot = RAGChatbot()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'RAG Chatbot API'
    })

@api_bp.route('/add_document', methods=['POST'])
def add_document():
    """Add a single document to the vector store"""
    try:
        data = request.get_json()
        validated_data = validate_add_document(data)
        
        doc_id = chatbot.add_document(
            validated_data['text'],
            validated_data['metadata']
        )
        
        return jsonify({
            'success': True,
            'doc_id': doc_id,
            'message': 'Document added successfully'
        })
    
    except ValidationError as e:
        logger.warning(f"Validation error in add_document: {str(e)}")
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        logger.error(f"Error in add_document: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/add_documents', methods=['POST'])
def add_documents():
    """Add multiple documents to the vector store"""
    try:
        data = request.get_json()
        validated_data = validate_add_documents(data)
        
        doc_ids = chatbot.add_documents_batch(
            validated_data['documents'],
            validated_data['metadatas']
        )
        
        return jsonify({
            'success': True,
            'doc_ids': doc_ids,
            'count': len(doc_ids),
            'message': f'Added {len(doc_ids)} documents successfully'
        })
    
    except ValidationError as e:
        logger.warning(f"Validation error in add_documents: {str(e)}")
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        logger.error(f"Error in add_documents: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        validated_data = validate_chat_request(data)
        
        result = chatbot.chat(
            validated_data['query'],
            validated_data['conversation_id'],
            validated_data['n_results']
        )
        
        return jsonify({
            'success': True,
            **result
        })
    
    except ValidationError as e:
        logger.warning(f"Validation error in chat: {str(e)}")
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/retrieve', methods=['POST'])
def retrieve():
    """Retrieve relevant documents for a query"""
    try:
        data = request.get_json()
        validated_data = validate_retrieve_request(data)
        
        results = chatbot.retrieve_documents(
            validated_data['query'],
            validated_data['n_results']
        )
        
        return jsonify({
            'success': True,
            'query': validated_data['query'],
            'results': results
        })
    
    except ValidationError as e:
        logger.warning(f"Validation error in retrieve: {str(e)}")
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        logger.error(f"Error in retrieve: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/collection_info', methods=['GET'])
def collection_info():
    """Get information about the collection"""
    try:
        info = chatbot.get_collection_info()
        return jsonify(info)
    
    except Exception as e:
        logger.error(f"Error in collection_info: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history"""
    try:
        history = chatbot.get_conversation_history(conversation_id)
        return jsonify(history)
    
    except Exception as e:
        logger.error(f"Error in get_conversation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/conversations', methods=['GET'])
def list_conversations():
    """List all conversation IDs"""
    try:
        conversation_ids = chatbot.get_all_conversations()
        return jsonify({
            'conversation_ids': conversation_ids,
            'count': len(conversation_ids)
        })
    
    except Exception as e:
        logger.error(f"Error in list_conversations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500