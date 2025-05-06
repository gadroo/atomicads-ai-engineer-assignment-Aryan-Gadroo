#!/usr/bin/env python

import os
import sys
import logging
import argparse
from pathlib import Path
import re
import time

# Add the project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.rag_service import RAGService
from src.models.openai_service import OpenAIService

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def chunk_text(text, max_chunk_size=1000, overlap=200):
    """Split text into chunks with overlap.
    
    Args:
        text: The text to split
        max_chunk_size: Maximum size of each chunk
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Split into paragraphs first
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed max size, add current chunk to list
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            chunks.append(current_chunk)
            # Keep overlap from previous chunk
            current_chunk = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
        
        # Add paragraph to current chunk
        if current_chunk and not current_chunk.endswith("\n"):
            current_chunk += "\n\n"
        current_chunk += paragraph
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def ingest_file(rag_service, file_path):
    """Ingest a file into the vector database.
    
    Args:
        rag_service: RAG service instance
        file_path: Path to the file to ingest
        
    Returns:
        int: Number of chunks ingested
    """
    try:
        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Get the file name for metadata
        file_name = Path(file_path).name
        
        # Extract title from Markdown content (assuming first # heading is title)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_name
        
        # Chunk the content
        chunks = chunk_text(content)
        
        # Create metadata for the document
        base_metadata = {
            "source": file_name,
            "title": title,
            "file_path": str(file_path),
            "chunk_index": 0,
            "total_chunks": len(chunks)
        }
        
        # Ingest each chunk
        for i, chunk in enumerate(chunks):
            metadata = {**base_metadata, "chunk_index": i}
            success = rag_service.add_document(chunk, metadata)
            
            if not success:
                logger.error(f"Failed to ingest chunk {i} of {file_path}")
        
        logger.info(f"Ingested {len(chunks)} chunks from {file_path}")
        return len(chunks)
    
    except Exception as e:
        logger.error(f"Error ingesting file {file_path}: {str(e)}")
        return 0

def ingest_directory(rag_service, directory_path, file_extensions=None):
    """Recursively ingest all files in a directory.
    
    Args:
        rag_service: RAG service instance
        directory_path: Path to the directory to ingest
        file_extensions: List of file extensions to ingest, or None for all
        
    Returns:
        tuple: (num_files_ingested, num_chunks_ingested)
    """
    try:
        directory = Path(directory_path)
        
        if not directory.exists() or not directory.is_dir():
            logger.error(f"{directory_path} does not exist or is not a directory")
            return 0, 0
        
        num_files_ingested = 0
        num_chunks_ingested = 0
        
        # Walk through the directory
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                
                # Skip if file extension doesn't match
                if file_extensions and not any(file.endswith(ext) for ext in file_extensions):
                    continue
                
                # Ingest the file
                chunks_ingested = ingest_file(rag_service, file_path)
                
                if chunks_ingested > 0:
                    num_files_ingested += 1
                    num_chunks_ingested += chunks_ingested
        
        return num_files_ingested, num_chunks_ingested
    
    except Exception as e:
        logger.error(f"Error ingesting directory {directory_path}: {str(e)}")
        return 0, 0

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Ingest knowledge base files into vector database")
    parser.add_argument("--dir", "-d", type=str, default="data/knowledge_base",
                        help="Directory containing knowledge base files")
    parser.add_argument("--extensions", "-e", type=str, default=".md,.txt",
                        help="Comma-separated list of file extensions to ingest")
    parser.add_argument("--reset", "-r", action="store_true",
                        help="Reset the vector database before ingesting")
    
    args = parser.parse_args()
    
    try:
        # Initialize services
        rag_service = RAGService()
        
        # Reset vector database if requested
        if args.reset:
            logger.info("Resetting vector database...")
            rag_service.vector_store.delete_all()
            time.sleep(1)  # Allow time for deletion to complete
        
        # Parse file extensions
        extensions = args.extensions.split(",") if args.extensions else None
        
        # Ingest directory
        start_time = time.time()
        num_files, num_chunks = ingest_directory(rag_service, args.dir, extensions)
        end_time = time.time()
        
        # Print summary
        logger.info(f"Ingestion complete in {end_time - start_time:.2f} seconds")
        logger.info(f"Ingested {num_files} files with {num_chunks} total chunks")
        
    except Exception as e:
        logger.exception("Error during ingestion")
        sys.exit(1)

if __name__ == "__main__":
    main() 