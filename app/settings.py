from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

@lru_cache
def get_settings():
    return Settings()

class Settings(BaseSettings):
    database_url: str
    debug: bool 
    enable_metrics:bool
    secret_key:str
    algorithm:str
    access_token_expire_minutes:str
    
    model_config = SettingsConfigDict(env_file=".env")
