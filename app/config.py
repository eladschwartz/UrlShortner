from pydantic_settings import BaseSettings
from .enums import Environment

class Settings(BaseSettings):
    ENVIRONMENT: Environment
    
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    origins_dev: str = "http://127.0.0.1:8000,'http://localhost:8000"
    origins_prod: str
    
    class Config:
        env_file=".env"
    
    @property
    def origins(self) -> list[str]:
        if self.ENVIRONMENT == Environment.DEVELOPMENT:
            return [origin.strip() for origin in self.origins_dev.split(",")]
        else:
            return [origin.strip() for origin in self.origins_prod.split(",")]
        
    
    
settings = Settings()


