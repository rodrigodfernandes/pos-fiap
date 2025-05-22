from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Optional
import os
import logging
import uuid
from datetime import datetime
from src.scraper.embrapa_scraper import run_scraper
from src.tasks.jobs import run_scraper_task_bg

router = APIRouter()
logger = logging.getLogger(__name__)

# Diretório padrão para salvar os dados
DEFAULT_OUTPUT_DIR = "data/vitibrasil"

# Sistema de rastreamento de tarefas em memória
task_status = {}

@router.get("/executar")
async def executar_sincrono(output_dir: Optional[str] = DEFAULT_OUTPUT_DIR):
    """
    Executa o scraping de forma síncrona
    """
    try:
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

@router.get("/executar_async")
async def executar_async(
    background_tasks: BackgroundTasks,
    output_dir: Optional[str] = DEFAULT_OUTPUT_DIR
):
    """
    Executa o scraping em background usando BackgroundTasks (assíncrono)
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Cria um ID único para a tarefa
        task_id = str(uuid.uuid4())
        
        # Inicializa o status da tarefa
        task_status[task_id] = {
            "task_id": task_id,
            "status": "pendente",
            "start_time": datetime.now(),
            "output_dir": output_dir
        }
        
        # Adiciona a tarefa ao background
        background_tasks.add_task(
            process_scraper_async, 
            task_id=task_id, 
            output_dir=output_dir
        )
        
        return {
            "status": "tarefa iniciada",
            "task_id": task_id,
            "output_dir": output_dir
        }
    except Exception as e:
        logger.error(f"Erro na execução assíncrona: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_scraper_async(task_id: str, output_dir: str):
    """
    Processa o scraper de forma assíncrona
    """
    try:
        # Atualiza status para "em andamento"
        task_status[task_id]["status"] = "em_andamento"
        
        # Executa o scraper
        results = run_scraper_task_bg(output_dir=output_dir)
        
        # Atualiza status para "concluído"
        task_status[task_id]["status"] = "concluído"
        task_status[task_id]["end_time"] = datetime.now()
        task_status[task_id]["results"] = results
        
        return results
    except Exception as e:
        logger.error(f"Erro no processamento assíncrono: {str(e)}")
        task_status[task_id]["status"] = "erro"
        task_status[task_id]["end_time"] = datetime.now()
        task_status[task_id]["error"] = str(e)
        return None

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Retorna o status atual de uma tarefa assíncrona
    """
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return task_status[task_id]

@router.get("/tarefas")
async def listar_tarefas():
    """
    Lista todas as tarefas e seus status
    """
    return task_status
