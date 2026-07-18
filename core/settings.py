from pydantic_settings import BaseSettings
from hyperlocal_platform.core.enums.environment_enum import EnvironmentEnum
from .constants import ENV_PREFIX
from dotenv import load_dotenv
load_dotenv()

class InventorySettings(BaseSettings):
    PG_DATABASE_URL:str
    ENVIRONMENT:EnvironmentEnum
    MONGO_DB_URL:str
    MINIO_ENDPOINT:str
    MINIO_ACCESS_KEY:str
    MINIO_SECRET_KEY:str
    MINIO_SECURE:bool = True
    RABBITMQ_HOST:str
    RABBITMQ_PORT:int
    RABBITMQ_LOGIN:str
    RABBITMQ_PASSWORD:str
    
    model_config={
        'case_sensitive':False,
        'env_prefix':ENV_PREFIX
    }