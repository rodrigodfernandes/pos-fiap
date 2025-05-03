from fastapi import APIRouter
from src.api.endpoints import scraper
from src.api.endpoints import data

# Criar um router principal que agregará todos os outros
router = APIRouter()

# Incluir o router de scraping
router.include_router(
    scraper.router,
    prefix="/scraper",
    tags=["scraping"]
)

router.include_router(data.router, prefix="/data", tags=["data"])
