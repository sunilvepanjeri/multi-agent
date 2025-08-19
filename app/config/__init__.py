from pydantic_settings import BaseSettings
import os
from dotenv import find_dotenv



class Settings(BaseSettings):

    OPENAI_API_KEY: str
    COLLECTION_NAME: str = 'rag'
    MODEL: str = 'gpt-4.1',
    EMBEDDING_MODEL: str = 'text-embedding-3-small'

    model_config = {'extra': 'allow'}

settings = Settings(_env_file=find_dotenv('.env'))

print(settings.model_dump())


os.environ.update(settings.model_dump())


