from fastapi import APIRouter
from src.api.endpoints import scraper

# Criar um router principal que agregará todos os outros
router = APIRouter()

# Incluir o router de scraping
router.include_router(
    scraper.router,
    prefix="/scraper",
    tags=["scraping"]
)