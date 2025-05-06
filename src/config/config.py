import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

class OpenAIConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = Field(default="gpt-4o-mini")
    embedding_model: str = Field(default="text-embedding-ada-002")
    max_tokens: int = Field(default=4000)
    temperature: float = Field(default=0.2)

class PineconeConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv("PINECONE_API_KEY", ""))
    environment: str = Field(default_factory=lambda: os.getenv("PINECONE_ENVIRONMENT", ""))
    index_name: str = Field(default_factory=lambda: os.getenv("PINECONE_INDEX", "ad-campaign-knowledge"))
    namespace: str = Field(default="default")

class MetaAdsConfig(BaseModel):
    app_id: str = Field(default_factory=lambda: os.getenv("META_APP_ID", ""))
    app_secret: str = Field(default_factory=lambda: os.getenv("META_APP_SECRET", ""))
    access_token: str = Field(default_factory=lambda: os.getenv("META_ACCESS_TOKEN", ""))
    ad_account_id: str = Field(default_factory=lambda: os.getenv("META_AD_ACCOUNT_ID", ""))
    business_id: str = Field(default_factory=lambda: os.getenv("META_BUSINESS_ID", ""))

class AppConfig(BaseModel):
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    pinecone: PineconeConfig = Field(default_factory=PineconeConfig)
    meta_ads: MetaAdsConfig = Field(default_factory=MetaAdsConfig)
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "False").lower() == "true")
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

# Create a global config instance
config = AppConfig() 