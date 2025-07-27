import os
import shutil
from typing import List, Dict, Any, Optional
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from services.file_processor import FileProcessor
from services.vector_store import VectorStore
from utils.logger import setup_logger
from config import Config

logger = setup_logger(__name__)

class FileManager:
    def __init__(self, vector_store: VectorStore):
        """Initialize file manager"""
        self.vector_store = vector_store
        self.file_processor = FileProcessor()
        self.upload_folder = Config.UPLOAD_FOLDER
        
        # Create upload directory if it doesn't exist
        Path(self.upload_folder).mkdir(parents=True, exist_ok=True)
        
        # Track uploaded files (in production, use database)
        self.uploaded_files = {}  # {file_hash: file_info}
        
        logger.info(f"File manager initialized. Upload folder: {self.upload_folder}")
    
    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        if not filename:
            return False
        
        extension = Path(filename).suffix.lower().lstrip('.')
        return extension in Config.ALLOWED_EXTENSIONS
    
    def upload_and_process_file(self, file: FileStorage, 
                               custom_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Upload file, process it, and add to vector store"""
        try:
            # Validate file
            if not file or not file.filename:
                raise ValueError("No file provided")
            
            if not self.is_allowed_file(file.filename):
                raise ValueError(f"File type not allowed. Supported types: {', '.join(Config.ALLOWED_EXTENSIONS)}")
            
            # Secure filename
            filename = secure_filename(file.filename)
            if not filename:
                raise ValueError("Invalid filename")
            
            # Save file temporarily
            temp_file_path = os.path.join(self.upload_folder, filename)
            file.save(temp_file_path)
            
            try:
                # Get file info and check for duplicates
                file_info = self.file_processor.get_file_info(temp_file_path, filename)
                
                if Config.ENABLE_DUPLICATE_DETECTION:
                    if file_info['file_hash'] in self.uploaded_files:
                        existing_file = self.uploaded_files[file_info['file_hash']]
                        logger.info(f"Duplicate file detected: {filename} (matches {existing_file['filename']})")
                        return {
                            'success': False,
                            'message': f'Duplicate file. Already uploaded as: {existing_file["filename"]}',
                            'existing_file': existing_file
                        }
                
                # Process file into chunks
                chunks = self.file_processor.process_file(temp_file_path, filename, custom_metadata)
                
                # Add chunks to vector store
                doc_ids = []
                documents = []
                metadatas = []
                
                for chunk_data in chunks:
                    documents.append(chunk_data['text'])
                    metadatas.append(chunk_data['metadata'])
                
                # Batch add to vector store
                doc_ids = self.vector_store.add_documents_batch(documents, metadatas)
                
                # Update file tracking
                file_record = {
                    **file_info,
                    'doc_ids': doc_ids,
                    'total_chunks': len(chunks),
                    'processing_status': 'completed'
                }
                
                self.uploaded_files[file_info['file_hash']] = file_record
                
                logger.info(f"Successfully processed {filename}: {len(chunks)} chunks, {len(doc_ids)} documents added")
                
                return {
                    'success': True,
                    'message': f'File {filename} processed successfully',
                    'file_info': file_record,
                    'chunks_created': len(chunks),
                    'documents_added': len(doc_ids)
                }
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                    
        except Exception as e:
            logger.error(f"Error uploading and processing file: {str(e)}")
            raise
    
    def upload_multiple_files(self, files: List[FileStorage], 
                             custom_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Upload and process multiple files"""
        results = []
        total_chunks = 0
        total_documents = 0
        
        for file in files:
            try:
                result = self.upload_and_process_file(file, custom_metadata)
                results.append(result)
                
                if result['success']:
                    total_chunks += result['chunks_created']
                    total_documents += result['documents_added']
                    
            except Exception as e:
                results.append({
                    'success': False,
                    'filename': file.filename if file else 'Unknown',
                    'error': str(e)
                })
        
        return {
            'success': True,
            'total_files_processed': len([r for r in results if r['success']]),
            'total_chunks_created': total_chunks,
            'total_documents_added': total_documents,
            'results': results
        }
    
    def get_uploaded_files(self) -> List[Dict[str, Any]]:
        """Get list of all uploaded files"""
        return list(self.uploaded_files.values())
    
    def delete_file_documents(self, file_hash: str) -> bool:
        """Delete all documents associated with a file"""
        try:
            if file_hash not in self.uploaded_files:
                return False
            
            file_record = self.uploaded_files[file_hash]
            doc_ids = file_record.get('doc_ids', [])
            
            # Delete documents from vector store
            for doc_id in doc_ids:
                self.vector_store.delete_document(doc_id)
            
            # Remove from tracking
            del self.uploaded_files[file_hash]
            
            logger.info(f"Deleted {len(doc_ids)} documents for file {file_record['filename']}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file documents: {str(e)}")
            return False
    
    def get_file_stats(self) -> Dict[str, Any]:
        """Get statistics about uploaded files"""
        total_files = len(self.uploaded_files)
        total_chunks = sum(f.get('total_chunks', 0) for f in self.uploaded_files.values())
        total_size = sum(f.get('file_size', 0) for f in self.uploaded_files.values())
        
        file_types = {}
        for file_info in self.uploaded_files.values():
            ext = file_info.get('file_extension', 'unknown')
            file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            'total_files': total_files,
            'total_chunks': total_chunks,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'file_types': file_types
        }