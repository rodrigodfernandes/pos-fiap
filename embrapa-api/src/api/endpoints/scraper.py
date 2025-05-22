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
    batch_size: Optional[int] = 5,
    sleep_between_batches: Optional[float] = 2.0,
    sleep_between_requests: Optional[float] = 0.5
):
    """
    Executa o scraping em background usando BackgroundTasks (assíncrono)
    
    - workers: Número de threads paralelas para processamento
    - batch_size: Quantidade de itens processados por lote
    - sleep_between_batches: Tempo de pausa entre lotes (segundos)
    - sleep_between_requests: Tempo de pausa entre requisições (segundos)
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
                "batch_size": batch_size,
                "sleep_between_batches": sleep_between_batches,
                "sleep_between_requests": sleep_between_requests
            }
        }
        
        # Adiciona a tarefa ao background
        background_tasks.add_task(
            process_scraper_async, 
            task_id=task_id, 
            output_dir=output_dir,
            workers=workers,
            batch_size=batch_size,
            sleep_between_batches=sleep_between_batches,
            sleep_between_requests=sleep_between_requests
        )
        
        return {
            "status": "tarefa iniciada",
            "task_id": task_id,
            "output_dir": output_dir,
            "config": {
                "workers": workers,
                "batch_size": batch_size,
                "sleep_between_batches": sleep_between_batches,
                "sleep_between_requests": sleep_between_requests
            }
        }
    except Exception as e:
        logger.error(f"Erro na execução assíncrona: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_scraper_async(
    task_id: str, 
    output_dir: str,
    workers: int = 3,
    batch_size: int = 5,
    sleep_between_batches: float = 2.0,
    sleep_between_requests: float = 0.5
):
    """
    Processa o scraper de forma assíncrona com paralelismo e controle de taxa
    """
    try:
        # Atualiza status para "em andamento"
        task_status[task_id]["status"] = "em_andamento"
        task_status[task_id]["progress"] = 0
        
        # Obtém a lista de itens a serem processados
        # Aqui você deve substituir esta lista de exemplo pelos itens reais a serem processados
        all_items = [f"item_{i}" for i in range(20)]  # Exemplo com 20 itens
        total_items = len(all_items)
        
        # Função para processar um único item
        def process_item(item):
            # Pausa entre requisições para não sobrecarregar o servidor
            time.sleep(sleep_between_requests)
            
            # Aqui viria o código real de processamento para cada item
            # Exemplo: resultados parciais para o item
            logger.info(f"Processando {item}...")
            return {"id": item, "resultado": f"Dados processados para {item}"}
        
        # Resultados de todos os itens
        all_results = []
        
        # Processar em lotes
        for batch_index in range(0, total_items, batch_size):
            # Seleciona o lote atual
            batch = all_items[batch_index:batch_index + batch_size]
            current_batch_size = len(batch)
            
            # Log do progresso
            progress_percent = (batch_index / total_items) * 100
            logger.info(f"Processando lote {batch_index//batch_size + 1}/{(total_items + batch_size - 1)//batch_size} - {progress_percent:.1f}%")
            task_status[task_id]["progress"] = progress_percent
            
            # Processa o lote atual em paralelo
            batch_results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                # Submete todas as tarefas do lote para execução
                future_to_item = {executor.submit(process_item, item): item for item in batch}
                
                # Processa os resultados à medida que são completados
                for future in concurrent.futures.as_completed(future_to_item):
                    item = future_to_item[future]
                    try:
                        result = future.result()
                        batch_results.append(result)
                        logger.info(f"Item {item} processado com sucesso")
                    except Exception as e:
                        logger.error(f"Erro ao processar item {item}: {str(e)}")
                        batch_results.append({"id": item, "status": "error", "error": str(e)})
            
            # Adiciona resultados deste lote ao total
            all_results.extend(batch_results)
            
            # Atualiza progresso
            task_status[task_id]["progress"] = ((batch_index + current_batch_size) / total_items) * 100
            
            # Pausa entre lotes
            if batch_index + batch_size < total_items:
                logger.info(f"Pausa de {sleep_between_batches} segundos antes do próximo lote...")
                time.sleep(sleep_between_batches)
        
        # Após processar todos os itens em lotes, chama a função principal do scraper
        # que pode usar os resultados pré-processados ou fazer o processamento final
        final_results = run_scraper_task_bg(output_dir=output_dir)
        
        # Mescla os resultados parciais com o resultado final
        results = {
            "status": "success",
            "items_processed": len(all_results),
            "partial_results": all_results,
            "final_results": final_results
        }
        
        # Atualiza status para "concluído"
        task_status[task_id]["status"] = "concluído"
        task_status[task_id]["end_time"] = datetime.now()
        task_status[task_id]["results"] = results
        task_status[task_id]["progress"] = 100
        
        return results
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
