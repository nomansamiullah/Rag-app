import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '500'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './data/chroma_db')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'documents')
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # RAG Configuration
    DEFAULT_N_RESULTS = int(os.getenv('DEFAULT_N_RESULTS', '5'))
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '10'))

    # File Upload Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '50')) * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx,doc,txt,md,csv,xlsx,xls').split(',')
    
    # Text Chunking Configuration
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
    MIN_CHUNK_SIZE = int(os.getenv('MIN_CHUNK_SIZE', '100'))
    
    # File Processing
    ENABLE_DUPLICATE_DETECTION = os.getenv('ENABLE_DUPLICATE_DETECTION', 'True').lower() == 'true'
    
    
    # File Upload Configuration (Increase limits)
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '100')) * 1024 * 1024  # 100MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    
    # Flask Upload Limits
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE  # Add this line