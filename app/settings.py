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
    pool_size:int
    max_overflow:int
    pool_timeout:int
    pool_recycle:int

    model_config = SettingsConfigDict(env_file=".env")
