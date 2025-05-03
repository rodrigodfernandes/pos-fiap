import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_scraper(output_dir="data/vitibrasil"):
    """
    Executa o scraping do VitiBrasil da Embrapa
    
    Args:
        output_dir: Diretório onde os dados serão salvos
    
    Returns:
        dict: Resultado da operação
    """
    # Garantir que o diretório de saída existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Lista de abas
    opcoes = ['opt_02', 'opt_03', 'opt_04', 'opt_05', 'opt_06']
    
    # URL
    base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao={}'
    
    # Resultados
    resultados = {}
    
    # Loop p/aba
    for opcao in opcoes:
        url = base_url.format(opcao)
        logger.info(f"Extraindo dados da aba {opcao}...")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table', class_='tb_base tb_dados')
            
            if tables:
                dataframes = []
                for table in tables:
                    df = pd.read_html(str(table))[0]
                    dataframes.append(df)
                
                final_df = pd.concat(dataframes, ignore_index=True)
                
                # Converter para JSON
                json_data = final_df.to_json(orient='records', force_ascii=False, indent=4)
                
                # Determinar o caminho do arquivo
                filename = os.path.join(output_dir, f'{opcao}.json')
                
                # Salvar em arquivo
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(json_data)
                
                logger.info(f'Dados da aba {opcao} salvos em {filename}')
                resultados[opcao] = {
                    'status': 'sucesso',
                    'arquivo': filename,
                    'registros': len(final_df)
                }
            else:
                logger.warning(f"Nenhuma tabela encontrada para {opcao}")
                resultados[opcao] = {
                    'status': 'aviso',
                    'mensagem': 'Nenhuma tabela encontrada'
                }
        else:
            logger.error(f'Erro na requisição da aba {opcao}: {response.status_code}')
            resultados[opcao] = {
                'status': 'erro',
                'mensagem': f'Erro HTTP {response.status_code}'
            }
    
    return resultados
