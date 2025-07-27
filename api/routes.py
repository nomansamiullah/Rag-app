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

from flask import request, jsonify
from werkzeug.utils import secure_filename
from services.file_manager import FileManager

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
        logger.info(f"Received data: {data}")  # Add this line
        
        validated_data = validate_add_document(data)
        logger.info(f"Validated data: {validated_data}")  # Add this line
        
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
        logger.error(f"FULL ERROR in add_document: {str(e)}")  # Add this line
        logger.error(f"ERROR TYPE: {type(e)}")  # Add this line
        import traceback
        logger.error(f"TRACEBACK: {traceback.format_exc()}")  # Add this line
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
    

# Initialize file manager
file_manager = FileManager(chatbot.vector_store)

@api_bp.route('/upload_file', methods=['POST'])
def upload_file():
    """Upload and process a single file"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get custom metadata from form data
        custom_metadata = {}
        if 'category' in request.form:
            custom_metadata['category'] = request.form['category']
        if 'tags' in request.form:
            custom_metadata['tags'] = request.form['tags']
        if 'description' in request.form:
            custom_metadata['description'] = request.form['description']
        
        # Process file
        result = file_manager.upload_and_process_file(file, custom_metadata)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 409  # Conflict (duplicate)
            
    except ValueError as e:
        logger.warning(f"Validation error in upload_file: {str(e)}")
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/upload_files', methods=['POST'])
def upload_files():
    """Upload and process multiple files"""
    try:
        files = request.files.getlist('files')
        
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files provided'}), 400
        
        # Get custom metadata
        custom_metadata = {}
        if 'category' in request.form:
            custom_metadata['category'] = request.form['category']
        if 'tags' in request.form:
            custom_metadata['tags'] = request.form['tags']
        
        # Process files
        result = file_manager.upload_multiple_files(files, custom_metadata)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in upload_files: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/uploaded_files', methods=['GET'])
def get_uploaded_files():
    """Get list of uploaded files"""
    try:
        files = file_manager.get_uploaded_files()
        return jsonify({
            'success': True,
            'files': files,
            'count': len(files)
        })
    except Exception as e:
        logger.error(f"Error in get_uploaded_files: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/file_stats', methods=['GET'])
def get_file_stats():
    """Get file upload statistics"""
    try:
        stats = file_manager.get_file_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Error in get_file_stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/delete_file/<file_hash>', methods=['DELETE'])
def delete_file(file_hash):
    """Delete all documents associated with a file"""
    try:
        success = file_manager.delete_file_documents(file_hash)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'File documents deleted successfully'
            })
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        logger.error(f"Error in delete_file: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500