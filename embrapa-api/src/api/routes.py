from fastapi import APIRouter
from src.config.database import SessionLocal
from passlib.context import CryptContext
from src.api.endpoints.auth import router as auth_router
from src.api.endpoints import scraper
from src.api.endpoints import data

# Criar um router principal que agregará todos os outros
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Login e geração de token
router.include_router(auth_router, prefix="/auth", tags=["auth"])

# Incluir o router de scraping
router.include_router(
    scraper.router,
    prefix="/scraper",
    tags=["scraping"]
)

router.include_router(data.router, prefix="/data", tags=["data"])

