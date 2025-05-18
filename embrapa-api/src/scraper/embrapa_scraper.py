import logging
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurar sessão com retry
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=60,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=['GET']
)
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

def fetch_html(url):
    response = session.get(url)
    if response.status_code == 200:
        logger.info(f"Sucesso ao acessar {url}")
        return response.text
    logger.error(f"Erro ao acessar {url}, status: {response.status_code}")
    return None

def extract_tables(html, source_label):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='tb_base tb_dados')
    dataframes = []
    for table in tables:
        df = pd.read_html(str(table))[0]
        df['type'] = source_label
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True) if dataframes else None

def process_option_principal(url, source_label, opt_key, output_dir):
    html = fetch_html(url)
    if html:
        df = extract_tables(html, source_label)
        if df is not None:
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, f"{opt_key}_completo.json")
            df.to_json(filename, orient='records', force_ascii=False, indent=4)
            logger.info(f"Salvo JSON: {filename}")

# Dicionário com os nomes das subopções
suboption_labels = {
    "opt_03": {
        "subopt_01": "Viníferas",
        "subopt_02": "Americanas e híbridas",
        "subopt_03": "Uvas de mesa"
    },
    "opt_05": {
        "subopt_01": "Vinhos de mesa",
        "subopt_02": "Espumantes",
        "subopt_03": "Uvas frescas",
        "subopt_04": "Uvas passas",
        "subopt_05": "Suco de uva"
    },
    "opt_06": {
        "subopt_01": "Vinhos de mesa",
        "subopt_02": "Espumantes",
        "subopt_03": "Uvas frescas",
        "subopt_04": "Suco de uva"
    }
}

def process_suboptions(urls, option_name, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    all_dfs = []

    for i, url in enumerate(urls, 1):
        subopt_id = f"subopt_0{i}"
        label = suboption_labels.get(option_name, {}).get(subopt_id, f"{option_name}_{subopt_id}")

        html = fetch_html(url)
        if html:
            df = extract_tables(html, label)
            if df is not None:
                all_dfs.append(df)

    if all_dfs:
        full_df = pd.concat(all_dfs, ignore_index=True)
        filename = os.path.join(output_dir, f"{option_name}_completo.json")
        full_df.to_json(filename, orient='records', force_ascii=False, indent=4)
        logger.info(f"Salvo JSON unificado: {filename}")
    else:
        logger.warning(f"Nenhuma tabela extraída para {option_name}")

options = {
    "opt_02": {
        "type": "principal",
        "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    },
    "opt_04": {
        "type": "principal",
        "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04"
    },
    "opt_03": {
        "type": "suboptions",
        "suburls": [
            f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_0{i}&opcao=opt_03" for i in range(1, 4)
        ]
    },
    "opt_05": {
        "type": "suboptions",
        "suburls": [
            f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_0{i}&opcao=opt_05" for i in range(1, 6)
        ]
    },
    "opt_06": {
        "type": "suboptions",
        "suburls": [
            f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_0{i}&opcao=opt_06" for i in range(1, 5)
        ]
    }
}

def run_scraper(output_dir="data/vitibrasil"):
    """
    Executa o scraping do VitiBrasil da Embrapa
    
    Args:
        output_dir: Diretório onde os dados serão salvos
    
    Returns:
        dict: Resultado da operação
    """
    os.makedirs(output_dir, exist_ok=True)
    resultados = {}

    for opt_key, opt_data in options.items():
        try:
            if opt_data["type"] == "principal":
                process_option_principal(opt_data["url"], "principal", opt_key, output_dir)
            elif opt_data["type"] == "suboptions":
                process_suboptions(opt_data["suburls"], opt_key, output_dir)
            resultados[opt_key] = {"status": "sucesso"}
        except Exception as e:
            logger.error(f"Erro no processamento da opção {opt_key}: {str(e)}")
            resultados[opt_key] = {"status": "falha", "erro": str(e)}

    return resultados


if __name__ == "__main__":
    resultados = run_scraper()
    print(resultados)
