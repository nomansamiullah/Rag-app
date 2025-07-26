from typing import Dict, List, Any
from utils.logger import setup_logger
from utils.helpers import generate_conversation_id

logger = setup_logger(__name__)

class ConversationManager:
    def __init__(self):
        """Initialize conversation manager"""
        # In production, use a proper database
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        logger.info("Initialized conversation manager")
    
    def get_or_create_conversation(self, conversation_id: str = None) -> str:
        """Get existing conversation or create new one"""
        if not conversation_id:
            conversation_id = generate_conversation_id()
            logger.info(f"Created new conversation: {conversation_id}")
        
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
            logger.info(f"Initialized conversation history for: {conversation_id}")
        
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """Add message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append({
            "role": role,
            "content": content
        })
        
        logger.debug(f"Added {role} message to conversation {conversation_id}")
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversations.get(conversation_id, [])
    
    def get_all_conversations(self) -> List[str]:
        """Get all conversation IDs"""
        return list(self.conversations.keys())
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Deleted conversation: {conversation_id}")
            return True
        return False
    
    def get_conversation_info(self, conversation_id: str) -> Dict[str, Any]:
        """Get conversation information"""
        history = self.get_conversation_history(conversation_id)
        return {
            'conversation_id': conversation_id,
            'message_count': len(history),
            'history': history
        }