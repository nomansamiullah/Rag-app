from flask import Flask
from flask_cors import CORS
from api.routes import api_bp
from utils.logger import setup_logger
from config import Config


# Setup logging
logger = setup_logger(__name__)

def create_app():
    """Application factory"""
    app = Flask(__name__)

    # Configure file uploads
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    logger.info("Flask application created successfully")
    return app

def main():
    """Main function to run the application"""
    try:
        app = create_app()
        
        logger.info("Starting RAG Chatbot Backend...")
        logger.info(f"ChromaDB Path: {Config.CHROMA_DB_PATH}")
        logger.info(f"Collection Name: {Config.COLLECTION_NAME}")
        logger.info("Available endpoints:")
        logger.info("  POST /add_document - Add single document")
        logger.info("  POST /add_documents - Add multiple documents")
        logger.info("  POST /chat - Chat with the bot")
        logger.info("  POST /retrieve - Retrieve relevant documents")
        logger.info("  GET /collection_info - Get collection information")
        logger.info("  GET /conversation/<id> - Get conversation history")
        logger.info("  GET /conversations - List all conversations")
        logger.info("  GET /health - Health check")
        
        app.run(
            debug=Config.FLASK_DEBUG,
            host=Config.FLASK_HOST,
            port=Config.FLASK_PORT
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

if __name__ == '__main__':
    main()