import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from utils.logger import setup_logger
from utils.helpers import generate_doc_id, add_timestamp_to_metadata
from config import Config

logger = setup_logger(__name__)

class VectorStore:
    def __init__(self):
        """Initialize ChromaDB vector store"""
        try:
            self.client = chromadb.PersistentClient(path=Config.CHROMA_DB_PATH)
            
            # Create or get collection
            try:
                self.collection = self.client.get_collection(name=Config.COLLECTION_NAME)
                logger.info(f"Loaded existing collection: {Config.COLLECTION_NAME}")
            except:
                self.collection = self.client.create_collection(name=Config.COLLECTION_NAME)
                logger.info(f"Created new collection: {Config.COLLECTION_NAME}")
                
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise
    
    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add single document to vector store"""
        try:
            doc_id = generate_doc_id()
            
            # Prepare metadata
            metadata = add_timestamp_to_metadata(metadata)
            metadata['doc_id'] = doc_id
            
            # Add to collection
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Added document with ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            raise
    
    def add_documents_batch(self, documents: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Add multiple documents to vector store"""
        try:
            doc_ids = [generate_doc_id() for _ in documents]
            
            if metadatas is None:
                metadatas = [{}] * len(documents)
            
            # Add timestamp and doc_id to each metadata
            for i, metadata in enumerate(metadatas):
                metadata = add_timestamp_to_metadata(metadata)
                metadata['doc_id'] = doc_ids[i]
                metadatas[i] = metadata
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=doc_ids
            )
            
            logger.info(f"Added {len(documents)} documents")
            return doc_ids
            
        except Exception as e:
            logger.error(f"Error adding documents batch: {str(e)}")
            raise
    
    def retrieve_documents(self, query: str, n_results: int = None) -> Dict[str, List]:
        """Retrieve relevant documents for a query"""
        try:
            if n_results is None:
                n_results = Config.DEFAULT_N_RESULTS
                
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else [],
                'distances': results['distances'][0] if results['distances'] else []
            }
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return {'documents': [], 'metadatas': [], 'distances': []}
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {
                'collection_name': Config.COLLECTION_NAME,
                'document_count': count,
                'database_path': Config.CHROMA_DB_PATH
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            raise
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID"""
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted document with ID: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {str(e)}")
            return False