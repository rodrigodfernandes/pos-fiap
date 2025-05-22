from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from typing import Dict, Optional, List
import os
import logging
import uuid
import time
import asyncio
import concurrent.futures
from datetime import datetime
from pydantic import BaseModel
from src.scraper.embrapa_scraper import run_scraper
from src.tasks.jobs import run_scraper_task_bg

router = APIRouter()
logger = logging.getLogger(__name__)

# Diretório padrão para salvar os dados
DEFAULT_OUTPUT_DIR = "data/vitibrasil"

# Sistema de rastreamento de tarefas em memória
# Na prática, isso deveria ser armazenado em um banco de dados
task_status = {}

class TaskStatus(BaseModel):
    task_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    progress: Optional[float] = 0.0
    results: Optional[Dict] = None
    error: Optional[str] = None

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

async def process_scraper_async(task_id: str, output_dir: str, sleep_time: float = 0.5, workers: int = 3):
    """
    Processa o scraper de forma assíncrona com paralelismo e sleep
    """
    try:
        # Atualiza status para "em andamento"
        task_status[task_id].status = "em_andamento"
        
        # Define a função que será executada em paralelo
        def scraper_worker(item):
            # Simula itens para scraping (substitua pela lógica real)
            time.sleep(sleep_time)  # Pausa para não sobrecarregar
            return f"Resultado para {item}"
        
        # Simula lista de itens para scraping (substitua pela lista real)
        items_to_scrape = [f"item_{i}" for i in range(10)]
        results = []
        
        # Executa o scraping com paralelismo
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(scraper_worker, item): item for item in items_to_scrape}
            total_items = len(items_to_scrape)
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                item = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    # Atualiza o progresso
                    progress = (i + 1) / total_items * 100
                    task_status[task_id].progress = progress
                except Exception as exc:
                    logger.error(f"Item {item} gerou uma exceção: {exc}")
        
        # Executa o scraper real com os resultados parciais já coletados
        final_results = run_scraper_task_bg(output_dir=output_dir)
        
        # Atualiza status para "concluído"
        task_status[task_id].status = "concluído"
        task_status[task_id].end_time = datetime.now()
        task_status[task_id].results = final_results
        
        return final_results
    except Exception as e:
        logger.error(f"Erro no processamento assíncrono: {str(e)}")
        task_status[task_id].status = "erro"
        task_status[task_id].end_time = datetime.now()
        task_status[task_id].error = str(e)
        return None

@router.post("/executar_async")
async def executar_async(
    background_tasks: BackgroundTasks,
    output_dir: Optional[str] = DEFAULT_OUTPUT_DIR,
    sleep_time: Optional[float] = 0.5,
    workers: Optional[int] = 3
):
    """
    Executa o scraping em background usando BackgroundTasks (assíncrono)
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Cria um ID único para a tarefa
        task_id = str(uuid.uuid4())
        
        # Inicializa o status da tarefa
        task_status[task_id] = TaskStatus(
            task_id=task_id,
            status="pendente",
            start_time=datetime.now()
        )
        
        # Adiciona a tarefa ao background
        background_tasks.add_task(
            process_scraper_async, 
            task_id=task_id, 
            output_dir=output_dir,
            sleep_time=sleep_time,
            workers=workers
        )
        
        return {
            "status": "tarefa iniciada",
            "task_id": task_id,
            "output_dir": output_dir,
            "message": "Consulte o status usando o endpoint /status/{task_id}"
        }
    except Exception as e:
        logger.error(f"Erro ao iniciar execução assíncrona: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Retorna o status atual de uma tarefa assíncrona
    """
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    task = task_status[task_id]
    
    return {
        "task_id": task.task_id,
        "status": task.status,
        "start_time": task.start_time,
        "end_time": task.end_time,
        "progress": task.progress,
        "results": task.results if task.status == "concluído" else None,
        "error": task.error if task.status == "erro" else None
    }

@router.get("/tarefas")
async def listar_tarefas():
    """
    Lista todas as tarefas e seus status
    """
    return [
        {
            "task_id": task_id,
            "status": info.status,
            "start_time": info.start_time,
            "progress": info.progress
        }
        for task_id, info in task_status.items()
    ]
