import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FIAP-Embrapa API"
    
    # Configurações do banco de dados
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "6432")  # Porta do PgBouncer
    DB_USER: str = os.getenv("DB_USER", "fiap-embrapa-app")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "fiap-embrapa-app")
    DB_NAME: str = os.getenv("DB_NAME", "fiap-embrapa")
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações da API da Embrapa
    EMBRAPA_API_URL: str = os.getenv("EMBRAPA_API_URL", "")
    EMBRAPA_API_KEY: str = os.getenv("EMBRAPA_API_KEY", "")

settings = Settings()


