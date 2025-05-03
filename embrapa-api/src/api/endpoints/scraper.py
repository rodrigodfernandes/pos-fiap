from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Optional
import os
import logging
import uuid
from src.scraper.embrapa_scraper import run_scraper

router = APIRouter()
logger = logging.getLogger(__name__)

# Diretório padrão para salvar os dados
DEFAULT_OUTPUT_DIR = "data/vitibrasil"


@router.get("/executar")
async def executar_sincrono(output_dir: Optional[str] = DEFAULT_OUTPUT_DIR):
    """
    Executa o scraping de forma síncrona
    """
    try:
        # Garantir que o diretório existe
        os.makedirs(output_dir, exist_ok=True)
            
        resultados = run_scraper(output_dir=output_dir)
        
        return {
            "status": "concluído",
            "resultados": resultados,
            "output_dir": output_dir
        }
    except Exception as e:
        logger.error(f"Erro na execução síncrona: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
