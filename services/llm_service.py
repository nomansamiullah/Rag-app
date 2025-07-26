from openai import OpenAI
from typing import List, Dict, Any
from utils.logger import setup_logger
from config import Config

logger = setup_logger(__name__)

class LLMService:
    def __init__(self):
        """Initialize OpenAI LLM service"""
        # Set all attributes first
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        
        # Then initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        logger.info(f"Initialized LLM service with model: {self.model}")
    
    def generate_response(self, query: str, context_docs: List[str], conversation_history: List[Dict[str, str]] = None) -> str:
        """Generate response using OpenAI with retrieved context"""
        try:
            # Prepare context
            context = "\n\n".join(context_docs) if context_docs else "No relevant context found."
            
            # Prepare system message
            system_message = {
                "role": "system",
                "content": f"""You are a helpful AI assistant. Use the following context to answer questions accurately and conversationally. 
                If the context doesn't contain relevant information, politely say so and provide a general helpful response.
                
                Context:
                {context}
                
                Instructions:
                - Be conversational and friendly
                - Use the context when relevant
                - If context is not sufficient, acknowledge it
                - Keep responses concise but informative
                """
            }
            
            # Prepare messages
            messages = [system_message]
            
            # Add conversation history (limited)
            if conversation_history:
                messages.extend(conversation_history[-Config.MAX_CONVERSATION_HISTORY:])
            
            # Add current query
            messages.append({"role": "user", "content": query})
            
            # CORRECTED: Generate response using NEW OpenAI v1.0+ format
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            generated_response = response.choices[0].message.content.strip()
            logger.info(f"Generated response for query: {query[:50]}...")
            
            return generated_response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again."
    
    def validate_api_key(self) -> bool:
        """Validate OpenAI API key"""
        try:
            # Try a simple API call with new format
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"Invalid OpenAI API key: {str(e)}")
            return False