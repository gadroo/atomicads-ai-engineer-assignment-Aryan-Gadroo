import json
import logging
import uuid
<<<<<<< HEAD
=======
import os
>>>>>>> e6be9c0 (output structure changes)
from typing import List, Dict, Any, Optional, Tuple

from src.models.openai_service import OpenAIService
from src.database.vector_store import VectorStore
from src.config.config import config

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.openai = OpenAIService()
        self.vector_store = VectorStore()
        
    def add_document(self, text: str, metadata: Dict[str, Any]) -> bool:
        """Add a document to the vector store.
        
        Args:
            text: The document text
            metadata: Metadata for the document
            
        Returns:
            bool: Success status
        """
        try:
            # Get embedding for the text
            embedding = self.openai.get_embedding(text)
            
            # Create a unique ID for the document
            doc_id = str(uuid.uuid4())
            
            # Create vector with metadata
            vector = {
                "id": doc_id,
                "values": embedding,
                "metadata": {
                    "text": text,
                    **metadata
                }
            }
            
            # Upsert to vector store
            return self.vector_store.upsert([vector])
        except Exception as e:
            logger.error(f"Failed to add document: {str(e)}")
            return False
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add multiple documents to the vector store.
        
        Args:
            documents: List of dictionaries with 'text' and 'metadata'
            
        Returns:
            bool: Success status
        """
        try:
            vectors = []
            
            for doc in documents:
                text = doc["text"]
                metadata = doc["metadata"]
                
                # Get embedding for the text
                embedding = self.openai.get_embedding(text)
                
                # Create a unique ID for the document
                doc_id = str(uuid.uuid4())
                
                # Create vector with metadata
                vector = {
                    "id": doc_id,
                    "values": embedding,
                    "metadata": {
                        "text": text,
                        **metadata
                    }
                }
                
                vectors.append(vector)
            
            # Upsert to vector store
            return self.vector_store.upsert(vectors)
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            return False
    
    def retrieve_relevant_context(
        self, 
        query: str, 
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query.
        
        Args:
            query: The query text
            top_k: Number of results to return
            filter: Optional filter for metadata
            
        Returns:
            List[Dict[str, Any]]: List of relevant documents with metadata
        """
        try:
            # Get embedding for the query
            query_embedding = self.openai.get_embedding(query)
            
            # Query vector store
            results = self.vector_store.query(
                query_vector=query_embedding,
                top_k=top_k,
                filter=filter
            )
            
            # Extract and return relevant documents with metadata
            documents = []
            for match in results.get("matches", []):
                documents.append({
                    "text": match["metadata"]["text"],
                    "metadata": {k: v for k, v in match["metadata"].items() if k != "text"},
                    "score": match["score"]
                })
            
            return documents
        except Exception as e:
            logger.error(f"Failed to retrieve context: {str(e)}")
            return []
    
    def generate_campaign(self, campaign_brief: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a campaign specification based on a brief.
        
        Args:
            campaign_brief: Dictionary containing campaign brief information
            
        Returns:
<<<<<<< HEAD
            Dict[str, Any]: Campaign specification
=======
            Dict[str, Any]: Campaign specification in Meta API format
>>>>>>> e6be9c0 (output structure changes)
        """
        try:
            # Convert campaign brief to a query string
            query = self._brief_to_query(campaign_brief)
            
            # Retrieve relevant context
            relevant_docs = self.retrieve_relevant_context(query)
            
            # Format context for the prompt
            context = self._format_context(relevant_docs)
            
            # Generate system message with context
            system_message = self._generate_system_message(context)
            
            # Format the user message with campaign brief
            user_message = self._format_user_message(campaign_brief)
            
            # Create messages array
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
            
            # Get completion with JSON response
            response = self.openai.get_completion(
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            # Parse and validate the response
            campaign_spec = json.loads(response)
            
<<<<<<< HEAD
=======
            # Ensure the response has the required Meta API structure
            if not self._validate_meta_api_structure(campaign_spec):
                raise ValueError("Generated campaign specification does not match Meta API structure")
            
>>>>>>> e6be9c0 (output structure changes)
            return campaign_spec
        except Exception as e:
            logger.error(f"Failed to generate campaign: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _brief_to_query(self, campaign_brief: Dict[str, Any]) -> str:
        """Convert campaign brief to a query string.
        
        Args:
            campaign_brief: Dictionary containing campaign brief information
            
        Returns:
            str: Query string
        """
        # Extract key information from brief for the query
        platform = campaign_brief.get("platform", "Meta")
        objective = campaign_brief.get("objective", "")
        product = campaign_brief.get("product_description", "")
        audience = campaign_brief.get("target_audience", "")
        
        # Construct query focusing on key aspects
        query = f"Create a {platform} ad campaign for {product} with objective {objective} targeting {audience}"
        
        return query
    
    def _format_context(self, documents: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context string.
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            str: Formatted context
        """
        context_parts = []
        
        for i, doc in enumerate(documents):
            text = doc["text"]
            metadata = doc["metadata"]
            source = metadata.get("source", "Unknown")
            
            context_parts.append(f"Document {i+1} from {source}:\n{text}\n")
        
        return "\n".join(context_parts)
    
    def _generate_system_message(self, context: str) -> str:
        """Generate system message with retrieved context.
        
        Args:
            context: Formatted context string
            
        Returns:
            str: System message
        """
        system_message = """You are an expert AI assistant integrated within a RAG-based campaign generation system. 
Your purpose is to help users create effective social media advertising campaigns with minimal input.

SYSTEM ARCHITECTURE CONTEXT:
- You operate within a Python application with modular architecture:
  1. User Interface Layer: CLI for campaign brief collection
  2. LLM Service Layer (you): Processes inputs with RAG-enhanced responses
  3. Ad Platform API Layer: Connects to social platforms (Meta, TikTok, LinkedIn)
  4. Validation Layer: Ensures data quality and platform compliance
  5. Logging & Monitoring: Tracks system performance and errors

RESPONSIBILITIES:
1. Analyze campaign briefs to understand business goals, target audience, budget constraints, and timelines
2. Generate complete campaign specifications using retrieved documentation
3. Structure outputs for direct API implementation
4. Validate all generated content against platform constraints
5. Provide reasoning for marketing decisions

CAMPAIGN STRUCTURE GUIDELINES:
- Ensure campaign names clearly reflect the product and objective
- Match optimization goals to the campaign objective (awareness → reach, sales → conversions)
- Set reasonable budgets based on industry benchmarks ($10-30/day for testing)
- Align targeting with the stated audience demographics and interests
- Use appropriate billing events and bid strategies for the chosen objective

QUALITY REQUIREMENTS:
- Ad copy should match the described brand voice
- Creative must emphasize key selling points from the brief
- Targeting should neither be too broad nor too narrow
- Recommendations should be backed by industry best practices
- Proposed strategy should align with the product's market positioning

OUTPUT FORMAT REQUIREMENTS:
- Provide complete, valid JSON with no missing required fields
- Include detailed reasoning for all major decisions
- Flag potential issues with the campaign brief
- Ensure all text adheres to platform character limits
- Use correct enum values for all platform-specific fields

USE RETRIEVED CONTEXT BY:
- Referencing specific sections of documentation when making recommendations
- Applying platform-specific best practices from the context
- Using terminology consistent with the Meta Ads platform
- Adapting recommendations based on industry benchmarks when available
- Incorporating targeting suggestions based on similar campaign types

Based on the campaign brief provided, you will generate a complete campaign specification in JSON format.

Here is relevant context from documentation that may help:

"""
        system_message += context
        return system_message
    
    def _format_user_message(self, campaign_brief: Dict[str, Any]) -> str:
        """Format user message with campaign brief.
        
        Args:
            campaign_brief: Dictionary containing campaign brief information
            
        Returns:
            str: Formatted user message
        """
        user_message = """Please create a complete campaign specification based on this brief:

"""
        # Add campaign brief details
        for key, value in campaign_brief.items():
            user_message += f"{key}: {value}\n"
        
        user_message += """
Respond with a complete campaign specification in JSON format with the following structure:
{
  "campaign": {
    "name": string,
    "objective": string,
    "special_ad_categories": [string],
    "budget_optimization": boolean,
    "status": string
  },
  "ad_set": {
    "name": string,
    "optimization_goal": string,
    "billing_event": string,
    "bid_strategy": string,
    "budget": {
      "amount": number,
      "type": string
    },
    "targeting": {
      "geo_locations": object,
      "age_min": number,
      "age_max": number,
      "genders": [number],
      "interests": [object],
      "exclusions": object,
      "custom_audiences": [object]
    },
    "schedule": {
      "start_time": string,
      "end_time": string
    }
  },
  "ad": {
    "name": string,
    "creative": {
      "title": string,
      "body": string,
      "call_to_action": string,
      "link": string,
      "image_description": string,
      "media_recommendations": string
    }
  },
  "reasoning": {
    "audience_analysis": string,
    "creative_strategy": string,
    "budget_rationale": string,
    "expected_performance": string,
    "documentation_references": [string]
  },
  "validation": {
    "potential_issues": [string],
    "compliance_status": boolean,
    "required_fields_missing": [string]
  }
}"""
        
        return user_message

    def query(self, query_text: str, top_k: int = 5) -> str:
        """Query the RAG system with a natural language question.
        
        Args:
            query_text: The question or query text
            top_k: Number of documents to retrieve
            
        Returns:
            str: Generated response that answers the query
        """
        try:
            # Retrieve relevant context
            context_chunks = self.retrieve_relevant_context(query_text, top_k=top_k)
            
            # Store the retrieved chunks for later access
            self.last_context_chunks = context_chunks
            
            # Format context for the prompt
            context = self._format_context(context_chunks)
            
            # Create system message
            system_message = f"""You are a knowledgeable assistant specialized in Meta/Facebook advertising best practices.
Use the following retrieved information to answer the user's question.
If you don't know the answer based on the provided information, say so - don't make up information.

Retrieved information:
{context}"""
            
            # Create messages for completion
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": query_text}
            ]
            
            # Get completion
            response = self.openai.get_completion(messages=messages)
            
            return response
            
        except Exception as e:
            logger.error(f"Error during query: {str(e)}")
<<<<<<< HEAD
            return f"An error occurred: {str(e)}" 
=======
            return f"An error occurred: {str(e)}" 

    def _validate_meta_api_structure(self, campaign_spec: Dict[str, Any]) -> bool:
        """Validate that the campaign specification matches Meta API structure.
        
        Args:
            campaign_spec: Campaign specification dictionary
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_sections = ["campaign", "ad_set", "ad"]
        required_campaign_fields = ["name", "objective", "status"]
        required_ad_set_fields = ["name", "optimization_goal", "billing_event", "bid_strategy", "budget", "targeting"]
        required_ad_fields = ["name", "creative"]
        
        # Check required sections
        if not all(section in campaign_spec for section in required_sections):
            return False
            
        # Check campaign fields
        if not all(field in campaign_spec["campaign"] for field in required_campaign_fields):
            return False
            
        # Check ad set fields
        if not all(field in campaign_spec["ad_set"] for field in required_ad_set_fields):
            return False
            
        # Check ad fields
        if not all(field in campaign_spec["ad"] for field in required_ad_fields):
            return False
            
        return True

    def save_campaign_spec(self, campaign_spec: Dict[str, Any], output_file: str) -> bool:
        """Save campaign specification to a JSON file.
        
        Args:
            campaign_spec: Campaign specification dictionary
            output_file: Path to output file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dir_name = os.path.dirname(output_file)
            if dir_name:  # Only make directories if there is a directory part
                os.makedirs(dir_name, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(campaign_spec, f, indent=2)
            logger.info(f"Campaign specification saved to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save campaign specification: {str(e)}")
            return False 
>>>>>>> e6be9c0 (output structure changes)
