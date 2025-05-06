import openai
import tiktoken
import logging
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from src.config.config import config

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        openai.api_key = config.openai.api_key
        self.model = config.openai.model
        self.embedding_model = config.openai.embedding_model
        self.max_tokens = config.openai.max_tokens
        self.temperature = config.openai.temperature
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding vector for a text.
        
        Args:
            text: The text to embed
            
        Returns:
            List[float]: The embedding vector
        """
        try:
            text = text.replace("\n", " ")
            response = openai.embeddings.create(
                input=[text],
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to get embedding: {str(e)}")
            raise
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embedding vectors for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        return [self.get_embedding(text) for text in texts]
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """Get completion from OpenAI.
        
        Args:
            messages: List of message dictionaries
            temperature: Temperature for completion (default from config)
            max_tokens: Max tokens for completion (default from config)
            response_format: Optional response format (e.g. {"type": "json_object"})
            
        Returns:
            str: Completion text
        """
        try:
            # Set defaults from config if not provided
            temperature = temperature if temperature is not None else self.temperature
            max_tokens = max_tokens if max_tokens is not None else self.max_tokens
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to get completion: {str(e)}")
            raise
    
    def num_tokens_from_string(self, string: str, model: Optional[str] = None) -> int:
        """Calculate the number of tokens in a string.
        
        Args:
            string: The string to calculate tokens for
            model: The model to use for tokenization (default from instance)
            
        Returns:
            int: Number of tokens
        """
        model = model or self.model
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(string)) 