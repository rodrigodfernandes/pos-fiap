from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Optional
import os
import logging
import uuid
from datetime import datetime
from src.scraper.embrapa_scraper import run_scraper
from src.tasks.jobs import run_scraper_task_bg
import concurrent.futures
import time

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
    output_dir: Optional[str] = DEFAULT_OUTPUT_DIR,
    workers: Optional[int] = 3,
    sleep_time: Optional[float] = 1.0
):
    """
    Executa o scraping em background usando BackgroundTasks (assíncrono)
    
    - workers: Número de threads paralelas para processamento
    - sleep_time: Tempo de pausa entre operações (segundos)
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
            "output_dir": output_dir,
            "progress": 0,
            "config": {
                "workers": workers,
                "sleep_time": sleep_time
            }
        }
        
        # Adiciona a tarefa ao background
        background_tasks.add_task(
            process_scraper_async, 
            task_id=task_id, 
            output_dir=output_dir,
            workers=workers,
            sleep_time=sleep_time
        )
        
        return {
            "status": "tarefa iniciada",
            "task_id": task_id,
            "output_dir": output_dir,
            "config": {
                "workers": workers,
                "sleep_time": sleep_time
            }
        }
    except Exception as e:
        logger.error(f"Erro na execução assíncrona: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_scraper_async(
    task_id: str, 
    output_dir: str,
    workers: int = 3,
    sleep_time: float = 5.0
):
    """
    Processa o scraper de forma assíncrona garantindo sleep entre cada parte processada.
    
    Args:
        task_id (str): Identificador único da tarefa
        output_dir (str): Diretório onde os dados serão salvos
        workers (int): Número de workers/partes a serem processadas
        sleep_time (float): Tempo de espera em segundos entre o processamento de cada parte
    
    Returns:
        dict: Resultado consolidado da operação ou None se ocorrer erro
    """
    try:
        # Atualiza status para "em andamento"
        task_status[task_id] = task_status.get(task_id, {})
        task_status[task_id]["status"] = "em_andamento"
        task_status[task_id]["progress"] = 0
        task_status[task_id]["start_time"] = datetime.now()
        
        # Simulando divisão do trabalho em partes
        parts = [f"parte_{i}" for i in range(workers)]
        total_parts = len(parts)
        results = []
        
        # Cria diretórios específicos para cada parte
        part_output_dirs = {part: os.path.join(output_dir, part) for part in parts}
        for part, part_dir in part_output_dirs.items():
            os.makedirs(part_dir, exist_ok=True)
        
        # Função para processar uma parte específica
        def process_part(part, part_output_dir):
            """Processa uma parte do trabalho"""
            logger.info(f"Processando {part}...")
            part_result = run_scraper_task_bg(output_dir=part_output_dir)
            
            return {
                "part": part,
                "result": part_result
            }
        
        # Processa cada parte de forma sequencial, com sleep entre elas
        completed = 0
        
        for part in parts:
            # Aplica sleep entre partes (exceto antes da primeira)
            if completed > 0:
                logger.info(f"Aguardando {sleep_time} segundos antes de processar a próxima parte...")
                time.sleep(sleep_time)
            
            # Processa a parte atual
            part_dir = part_output_dirs[part]
            try:
                result = process_part(part, part_dir)
                results.append(result)
                logger.info(f"Parte {part} concluída com sucesso")
            except Exception as e:
                logger.error(f"Erro ao processar parte {part}: {str(e)}")
                results.append({"part": part, "error": str(e)})
            
            # Atualiza o progresso
            completed += 1
            progress = (completed / total_parts) * 100
            task_status[task_id]["progress"] = progress
            logger.info(f"Progresso: {progress:.1f}%")
        
        # Após o processamento em sequência, combina os resultados
        logger.info("Combinando resultados de todas as partes...")
        
        # Isso pode ser útil para consolidar os resultados parciais
        final_result = run_scraper_task_bg(output_dir=output_dir)
        
        # Atualiza status para "concluído"
        consolidated_results = {
            "parts_results": results,
            "final_result": final_result
        }
        
        task_status[task_id]["status"] = "concluído"
        task_status[task_id]["end_time"] = datetime.now()
        task_status[task_id]["results"] = consolidated_results
        task_status[task_id]["progress"] = 100
        
        return consolidated_results
    except Exception as e:
        logger.error(f"Erro no processamento assíncrono: {str(e)}")
        task_status[task_id]["status"] = "erro"
        task_status[task_id]["end_time"] = datetime.now()
        task_status[task_id]["error"] = str(e)
        task_status[task_id]["progress"] = 0
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
