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
    Processa o scraper de forma assíncrona com paralelismo e sleep
    """
    try:
        # Atualiza status para "em andamento"
        task_status[task_id]["status"] = "em_andamento"
        task_status[task_id]["progress"] = 0
        
        # Simulando divisão do trabalho em partes (para demonstrar paralelismo)
        # Na implementação real, você pode dividir por categorias, regiões, etc.
        parts = [f"parte_{i}" for i in range(workers)]
        total_parts = len(parts)
        results = []
        
        def process_part(part, part_output_dir):
            """Processa uma parte do trabalho com sleep para não sobrecarregar"""
            logger.info(f"Processando {part}...")
            # Adiciona pausa para não sobrecarregar
            time.sleep(sleep_time)
            
            part_result = run_scraper_task_bg(output_dir=part_output_dir)
            
            return {
                "part": part,
                "result": part_result
            }
        
        # Usando ThreadPoolExecutor para paralelismo
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # Cria diretórios específicos para cada parte, desta forma evita lock nos arquivos
            # e permite que cada thread escreva em seu próprio diretório
            part_output_dirs = {part: os.path.join(output_dir, part) for part in parts}
            for part, part_dir in part_output_dirs.items():
                os.makedirs(part_dir, exist_ok=True)
            
            # Submete as tarefas para execução paralela
            futures = {
                executor.submit(process_part, part, part_dir): part 
                for part, part_dir in part_output_dirs.items()
            }
            
            # Processa os resultados à medida que são completados
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                part = futures[future]
                try:
                    result = future.result()
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
        
        # Após o processamento em paralelo, pode ser necessário combinar os resultados
        # Por exemplo, unir arquivos, consolidar dados, etc.
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
