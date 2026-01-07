from pydantic import BaseSettings
class Settings(BaseSettings):
     QDRANT_URL: str
     QDRANT_COLLECTION: str
     DATABASE_URL: str
     REDIS_URL: str
     OLLAMA_BASE_URL:str
     OLLAMA_MODE:str


     class Config:
        env_file = ".env"

settings = Settings()