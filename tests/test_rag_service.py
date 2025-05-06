import unittest
import json
from unittest.mock import patch, MagicMock
import os
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.rag_service import RAGService
from src.models.openai_service import OpenAIService
from src.database.vector_store import VectorStore

class TestRAGService(unittest.TestCase):
    
    @patch('src.models.openai_service.OpenAIService')
    @patch('src.database.vector_store.VectorStore')
    def setUp(self, mock_vector_store, mock_openai_service):
        # Set up mocks
        self.mock_openai = mock_openai_service.return_value
        self.mock_vector_store = mock_vector_store.return_value
        
        # Create RAG service with mocked dependencies
        self.rag_service = RAGService()
        self.rag_service.openai = self.mock_openai
        self.rag_service.vector_store = self.mock_vector_store
        
        # Set up test data
        self.test_campaign_brief = {
            "platform": "Meta",
            "product_name": "Test Product",
            "product_description": "A test product for unit testing",
            "objective": "OUTCOME_AWARENESS",
            "daily_budget": 10.0,
            "target_audience": "Test audience"
        }
        
        # Set up mock responses
        self.mock_documents = [
            {
                "text": "Test document 1",
                "metadata": {"source": "test_source_1"},
                "score": 0.95
            },
            {
                "text": "Test document 2",
                "metadata": {"source": "test_source_2"},
                "score": 0.85
            }
        ]
        
        self.mock_campaign_spec = {
            "campaign": {
                "name": "Test Campaign",
                "objective": "OUTCOME_AWARENESS",
                "status": "PAUSED"
            },
            "ad_set": {
                "name": "Test Ad Set",
                "optimization_goal": "REACH",
                "billing_event": "IMPRESSIONS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "budget": {"amount": 1000, "type": "daily"},
                "targeting": {"geo_locations": {"countries": ["US"]}}
            },
            "ad": {
                "name": "Test Ad",
                "creative": {
                    "title": "Test Title",
                    "body": "Test Body",
                    "call_to_action": "LEARN_MORE",
                    "link": "https://example.com"
                }
            }
        }
    
    def test_add_document(self):
        # Setup
        text = "Test document"
        metadata = {"source": "test_source"}
        self.mock_openai.get_embedding.return_value = [0.1, 0.2, 0.3]
        self.mock_vector_store.upsert.return_value = True
        
        # Execute
        result = self.rag_service.add_document(text, metadata)
        
        # Assert
        self.assertTrue(result)
        self.mock_openai.get_embedding.assert_called_once_with(text)
        self.mock_vector_store.upsert.assert_called_once()
    
    def test_retrieve_relevant_context(self):
        # Setup
        query = "Test query"
        self.mock_openai.get_embedding.return_value = [0.1, 0.2, 0.3]
        self.mock_vector_store.query.return_value = {
            "matches": [
                {
                    "metadata": {"text": "Test document 1", "source": "test_source_1"},
                    "score": 0.95
                },
                {
                    "metadata": {"text": "Test document 2", "source": "test_source_2"},
                    "score": 0.85
                }
            ]
        }
        
        # Execute
        results = self.rag_service.retrieve_relevant_context(query)
        
        # Assert
        self.assertEqual(len(results), 2)
        self.mock_openai.get_embedding.assert_called_once_with(query)
        self.mock_vector_store.query.assert_called_once()
    
    def test_generate_campaign(self):
        # Setup
        self.mock_openai.get_embedding.return_value = [0.1, 0.2, 0.3]
        self.mock_vector_store.query.return_value = {
            "matches": [
                {
                    "metadata": {"text": "Test document 1", "source": "test_source_1"},
                    "score": 0.95
                }
            ]
        }
        
        mock_response = json.dumps(self.mock_campaign_spec)
        self.mock_openai.get_completion.return_value = mock_response
        
        # Execute
        result = self.rag_service.generate_campaign(self.test_campaign_brief)
        
        # Assert
        self.assertEqual(result["campaign"]["name"], "Test Campaign")
        self.assertEqual(result["campaign"]["objective"], "OUTCOME_AWARENESS")
        self.mock_vector_store.query.assert_called_once()
        self.mock_openai.get_completion.assert_called_once()

if __name__ == '__main__':
    unittest.main() 