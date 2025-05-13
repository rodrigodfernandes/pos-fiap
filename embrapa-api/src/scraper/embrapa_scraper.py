import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging

def run_scraper(output_dir="data/vitibrasil"):
    """
    Executa o scraping do VitiBrasil da Embrapa
    
    Args:
        output_dir: Diretório onde os dados serão salvos
    
    Returns:
        dict: Resultado da operação
    """
    # Configuração de logging melhorada
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    # Garantir que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Configuração da sessão com retry
    session = requests.Session()
    try:
        retries = Retry(
            total=3,
            backoff_factor=60,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=['GET']  # Para versões mais recentes
        )
    except TypeError:
        retries = Retry(
            total=3,
            backoff_factor=60,
            status_forcelist=[500, 502, 503, 504],
            method_whitelist=['GET']  # Para versões mais antigas
        )
    
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # Lista de abas
    opcoes = ['opt_02', 'opt_03', 'opt_04', 'opt_05', 'opt_06']
    
    # URL base
    base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao={}'
    
    # Resultados
    resultados = {}
    
    # Loop p/aba
    for opcao in opcoes:
        url = base_url.format(opcao)
        logger.info(f"Extraindo dados da aba {opcao}...")
        
        try:
            # Obter HTML
            html = fetch_html(url, session, logger)
            
            # Extrair tabelas
            df = extract_tables(html, logger)
            
            if df is not None:
                # Determinar o caminho do arquivo
                filename = os.path.join(output_dir, f'{opcao}.json')
                
                # Salvar em arquivo
                save_json(df, filename, logger)
                
                logger.info(f'Dados da aba {opcao} salvos em {filename}')
                resultados[opcao] = {
                    'status': 'sucesso',
                    'arquivo': filename,
                    'registros': len(df)
                }
            else:
                logger.warning(f"Nenhuma tabela encontrada para {opcao}")
                resultados[opcao] = {
                    'status': 'aviso',
                    'mensagem': 'Nenhuma tabela encontrada'
                }
        except Exception as e:
            logger.exception(f"Erro ao processar {opcao}: {e}")
            resultados[opcao] = {
                'status': 'erro',
                'mensagem': f'Erro: {str(e)}'
            }
    
    return resultados

def fetch_html(url, session, logger):
    """
    Obtém o conteúdo HTML de uma URL usando a sessão fornecida
    
    Args:
        url: URL para acessar
        session: Sessão de requests configurada
        logger: Logger configurado
        
    Returns:
        str: Conteúdo HTML
        
    Raises:
        Exception: Se ocorrer algum erro
    """
    response = session.get(url)
    if response.status_code == 200:
        logger.info(f'Sucesso ao acessar {url}')
        return response.text
    logger.error(f'Erro ao acessar {url}, status: {response.status_code}')
    raise Exception(f'Erro ao acessar {url}, status: {response.status_code}')

def extract_tables(html, logger):
    """
    Extrai tabelas do HTML e converte em DataFrame
    
    Args:
        html: Conteúdo HTML
        logger: Logger configurado
        
    Returns:
        DataFrame ou None se não encontrar tabelas
    """
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='tb_base tb_dados')
    
    if not tables:
        logger.warning("Nenhuma tabela encontrada no HTML")
        return None
    
    dataframes = [pd.read_html(str(table))[0] for table in tables]
    return pd.concat(dataframes, ignore_index=True) if dataframes else None

def save_json(df, filename, logger):
    """
    Salva DataFrame como JSON
    
    Args:
        df: DataFrame a ser salvo
        filename: Nome do arquivo
        logger: Logger configurado
    """
    json_data = df.to_json(orient='records', force_ascii=False, indent=4)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_data)
    logger.info(f'Salvo arquivo JSON: {filename}')
