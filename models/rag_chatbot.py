from typing import Dict, List, Any, Optional
from services.vector_store import VectorStore
from services.llm_service import LLMService
from services.conversation_manager import ConversationManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

class RAGChatbot:
    def __init__(self):
        """Initialize RAG Chatbot with all services"""
        try:
            self.vector_store = VectorStore()
            self.llm_service = LLMService()
            self.conversation_manager = ConversationManager()
            
            logger.info("RAG Chatbot initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Chatbot: {str(e)}")
            raise
    
    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add document to vector store"""
        return self.vector_store.add_document(text, metadata)
    
    def add_documents_batch(self, documents: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Add multiple documents to vector store"""
        return self.vector_store.add_documents_batch(documents, metadatas)
    
    def retrieve_documents(self, query: str, n_results: int = None) -> Dict[str, List]:
        """Retrieve relevant documents"""
        return self.vector_store.retrieve_documents(query, n_results)
    
    def chat(self, query: str, conversation_id: str = None, n_results: int = None) -> Dict[str, Any]:
        """Main chat function"""
        try:
            # Get or create conversation
            conversation_id = self.conversation_manager.get_or_create_conversation(conversation_id)
            
            # Retrieve relevant documents
            retrieved_docs = self.retrieve_documents(query, n_results)
            
            # Get conversation history
            conversation_history = self.conversation_manager.get_conversation_history(conversation_id)
            
            # Generate response
            response = self.llm_service.generate_response(
                query,
                retrieved_docs['documents'],
                conversation_history
            )
            
            # Update conversation history
            self.conversation_manager.add_message(conversation_id, "user", query)
            self.conversation_manager.add_message(conversation_id, "assistant", response)
            
            logger.info(f"Processed chat for conversation: {conversation_id}")
            
            return {
                'response': response,
                'conversation_id': conversation_id,
                'retrieved_docs_count': len(retrieved_docs['documents']),
                'context_used': retrieved_docs['documents'][:2] if retrieved_docs['documents'] else []
            }
            
        except Exception as e:
            logger.error(f"Error in chat function: {str(e)}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get vector store collection info"""
        return self.vector_store.get_collection_info()
    
    def get_conversation_history(self, conversation_id: str) -> Dict[str, Any]:
        """Get conversation history"""
        return self.conversation_manager.get_conversation_info(conversation_id)
    
    def get_all_conversations(self) -> List[str]:
        """Get all conversation IDs"""
        return self.conversation_manager.get_all_conversations()