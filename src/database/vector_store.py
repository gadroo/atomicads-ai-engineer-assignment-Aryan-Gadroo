import pinecone
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from src.config.config import config
from pinecone import Pinecone, ServerlessSpec

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.index_name = config.pinecone.index_name
        self.namespace = config.pinecone.namespace
        self._initialize_pinecone()
        
    def _initialize_pinecone(self) -> None:
        """Initialize Pinecone client and ensure the index exists."""
        try:
            # Initialize Pinecone with the recommended approach
            self.pc = Pinecone(api_key=config.pinecone.api_key)
            
            # Check if index exists, create it if not
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            if self.index_name not in existing_indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logger.info(f"Created Pinecone index: {self.index_name}")
            
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Successfully connected to Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {str(e)}")
            raise
    
    def upsert(self, vectors: List[Dict[str, Any]]) -> bool:
        """Upsert vectors to Pinecone.
        
        Args:
            vectors: List of dictionaries with 'id', 'values', and 'metadata'
        
        Returns:
            bool: Success status
        """
        try:
            self.index.upsert(vectors=vectors, namespace=self.namespace)
            return True
        except Exception as e:
            logger.error(f"Failed to upsert vectors: {str(e)}")
            return False
    
    def query(
        self, 
        query_vector: List[float], 
        top_k: int = 5, 
        filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Query vectors from Pinecone.
        
        Args:
            query_vector: Embedding vector to query
            top_k: Number of results to return
            filter: Optional filter for metadata
            
        Returns:
            Dict containing query results
        """
        try:
            return self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                namespace=self.namespace,
                filter=filter
            )
        except Exception as e:
            logger.error(f"Failed to query vectors: {str(e)}")
            return {"matches": []}
    
    def delete(self, ids: List[str]) -> bool:
        """Delete vectors by ID.
        
        Args:
            ids: List of vector IDs to delete
            
        Returns:
            bool: Success status
        """
        try:
            self.index.delete(ids=ids, namespace=self.namespace)
            return True
        except Exception as e:
            logger.error(f"Failed to delete vectors: {str(e)}")
            return False
    
    def delete_all(self) -> bool:
        """Delete all vectors in the namespace.
        
        Returns:
            bool: Success status
        """
        try:
            # First check if namespace exists by doing a simple query
            try:
                self.index.query(
                    vector=[0] * 1536,
                    top_k=1,
                    namespace=self.namespace
                )
                # If query succeeds, proceed with deletion
                self.index.delete(delete_all=True, namespace=self.namespace)
                logger.info(f"Deleted all vectors in namespace: {self.namespace}")
                return True
            except Exception as e:
                # If namespace doesn't exist, it's already "empty"
                if "404" in str(e) or "Not Found" in str(e):
                    logger.info(f"Namespace {self.namespace} is empty or doesn't exist. Nothing to delete.")
                    return True
                else:
                    raise e
        except Exception as e:
            logger.error(f"Failed to delete all vectors: {str(e)}")
            return False 