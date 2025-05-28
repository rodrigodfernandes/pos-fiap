import os
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import chardet
import re
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# Labels das subopções
suboption_labels = {
    "opt_03": {
        "subopt_01": "Viníferas",
        "subopt_02": "Americanas e híbridas",
        "subopt_03": "Uvas de mesa",
        "subopt_04": "Sem classificação"
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

def fetch_csv_link(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    link_tag = soup.find('a', href=True, text=lambda x: x and 'CSV' in x.upper())
    if not link_tag:
        link_tag = soup.find('a', href=lambda href: href and 'csv' in href.lower())
    if link_tag:
        return urljoin(base_url, link_tag['href'])
    return None

def download_csv(csv_url, dest_path):
    response = session.get(csv_url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"CSV salvo em: {dest_path}")
    else:
        raise Exception(f"Erro ao baixar CSV. Status: {response.status_code}")

def detectar_separador_e_codificacao(filepath):
    with open(filepath, 'rb') as f:
        result = chardet.detect(f.read(2048))
    encoding = result['encoding'] or 'utf-8'
    if encoding.lower() == 'ascii':
        encoding = 'utf-8'
    with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
        amostra = [f.readline() for _ in range(5)]
        conteudo = ''.join(amostra)
        if conteudo.count(';') > conteudo.count('\t'):
            sep = ';'
        elif conteudo.count('\t') > conteudo.count(';'):
            sep = '\t'
        else:
            sep = ','
    return sep, encoding

def padronizar_csv(caminho_arquivo, caminho_saida, sep_padrao=';'):
    sep_detectado, encoding = detectar_separador_e_codificacao(caminho_arquivo)
    df = pd.read_csv(caminho_arquivo, sep=sep_detectado, encoding=encoding)

    # Corrigir colunas "1970.1", "1980.1" para "1970", "1980"
    df.columns = [re.sub(r'^(\d{4})\.\d+$', r'\1', str(col)) for col in df.columns]

    # Detectar colunas que são anos
    colunas_ano = [col for col in df.columns if str(col).isdigit()]
    colunas_id = [col for col in df.columns if col not in colunas_ano]

    if colunas_ano:
        df = df.melt(
            id_vars=colunas_id,
            value_vars=colunas_ano,
            var_name='ano',
            value_name='valor'
        )

        # Corrigir extração de opt_key com regex
        match = re.search(r'(opt_\d{2})', os.path.basename(caminho_saida))
        opt_key = match.group(1) if match else ''

        label_por_opt = {
            "opt_02": "Quantidade (L.)",
            "opt_03": "Quantidade (Kg)",
            "opt_04": "Quantidade (L.)",
            "opt_05": "Quantidade (Kg)",
            "opt_06": "Quantidade (Kg)"
        }

        novo_nome_valor = label_por_opt.get(opt_key, "valor")
        df.rename(columns={"valor": novo_nome_valor}, inplace=True)

    df.to_csv(caminho_saida, sep=sep_padrao, index=False, encoding='utf-8')
    logger.info(f"CSV padronizado e transformado salvo em: {caminho_saida}")


def process_principal_option(opt_key, url, output_dir):
    html = session.get(url).text
    csv_url = fetch_csv_link(html, url)
    if not csv_url:
        raise Exception("Link para CSV não encontrado.")
    os.makedirs(output_dir, exist_ok=True)
    temp_path = os.path.join(output_dir, f"{opt_key}_temp.csv")
    final_path = os.path.join(output_dir, f"{opt_key}.csv")
    download_csv(csv_url, temp_path)
    padronizar_csv(temp_path, final_path)
    os.remove(temp_path)

def process_suboptions(opt_key, output_dir):
    suboptions = suboption_labels.get(opt_key, {})
    total = len(suboptions)
    for i in range(1, total + 1):
        sub_id = f"subopt_0{i}"
        label = suboptions.get(sub_id, sub_id)
        sub_url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao={sub_id}&opcao={opt_key}"
        logger.info(f"Acessando {sub_url} ({label})")

        html = session.get(sub_url).text
        csv_url = fetch_csv_link(html, sub_url)
        if not csv_url:
            logger.warning(f"Nenhum CSV encontrado em {sub_url}")
            continue

        opt_dir = os.path.join(output_dir, opt_key)
        os.makedirs(opt_dir, exist_ok=True)
        temp_path = os.path.join(opt_dir, f"{opt_key}_{label}_temp.csv".replace(" ", "_"))
        final_path = os.path.join(opt_dir, f"{opt_key}_{label}.csv".replace(" ", "_"))
        download_csv(csv_url, temp_path)
        padronizar_csv(temp_path, final_path)
        os.remove(temp_path)

def converter_csvs_para_json(diretorio_base):
    for root, _, files in os.walk(diretorio_base):
        for file in files:
            if file.endswith(".csv"):
                caminho_csv = os.path.join(root, file)
                caminho_json = os.path.splitext(caminho_csv)[0] + ".json"
                sep_detectado, encoding = detectar_separador_e_codificacao(caminho_csv)
                df = pd.read_csv(caminho_csv, sep=sep_detectado, encoding=encoding)

                # Remover colunas 'id' e 'control' (case-insensitive)
                colunas_para_remover = [col for col in df.columns if col.lower() in ["id", "control"]]
                df.drop(columns=colunas_para_remover, inplace=True, errors='ignore')

                # Corrigir o nome da coluna "Pa√≠s" para "País"
                df.columns = [col.replace("Pa√≠s", "País") for col in df.columns]

                # Inferir tipo
                tipo = "principal"
                partes = file.split('_')
                for opt, subs in suboption_labels.items():
                    for sub_id, sub_label in subs.items():
                        if sub_label in file:
                            tipo = sub_label

                df.insert(0, "type", tipo)
                df.to_json(caminho_json, orient='records', force_ascii=False, indent=2)
                logger.info(f"Convertido para JSON: {caminho_json}")



def juntar_jsons_por_opcao(diretorio_base, opcoes_agrupadas=["opt_03", "opt_05", "opt_06"]):
    for opt_key in opcoes_agrupadas:
        opt_path = os.path.join(diretorio_base, opt_key)
        if not os.path.exists(opt_path):
            logger.warning(f"Pasta não encontrada: {opt_path}")
            continue

        registros_total = []
        for file in os.listdir(opt_path):
            if file.endswith(".json"):
                caminho_json = os.path.join(opt_path, file)
                try:
                    with open(caminho_json, encoding='utf-8') as f:
                        dados = json.load(f)
                        registros_total.extend(dados)
                except Exception as e:
                    logger.error(f"Erro ao ler {caminho_json}: {str(e)}")

        if registros_total:
            caminho_saida = os.path.join(diretorio_base, f"{opt_key}.json")
            with open(caminho_saida, "w", encoding='utf-8') as f_out:
                json.dump(registros_total, f_out, ensure_ascii=False, indent=2)
            logger.info(f"Arquivo JSON combinado salvo: {caminho_saida}")
        else:
            logger.warning(f"Nenhum dado encontrado para juntar em {opt_key}")

def run_csv_downloader(output_dir="data/vitibrasil"):
    os.makedirs(output_dir, exist_ok=True)
    options = {
        "opt_02": "principal",
        "opt_04": "principal",
        "opt_03": "suboptions",
        "opt_05": "suboptions",
        "opt_06": "suboptions"
    }
    resultados = {}
    for opt_key, opt_type in options.items():
        try:
            logger.info(f"Processando {opt_key} ({opt_type})...")
            if opt_type == "principal":
                url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao={opt_key}"
                process_principal_option(opt_key, url, os.path.join(output_dir, opt_key))
            elif opt_type == "suboptions":
                process_suboptions(opt_key, output_dir)
            resultados[opt_key] = {"status": "sucesso"}
        except Exception as e:
            logger.error(f"Erro ao processar {opt_key}: {str(e)}")
            resultados[opt_key] = {"status": "falha", "erro": str(e)}
    return resultados

def run_scraper(output_dir="data/vitibrasil"):
    """
    Executa o scraping do VitiBrasil da Embrapa, realizando o download,
    padronização e conversão dos dados para JSON.
    
    Args:
        output_dir: Diretório onde os dados serão salvos
    
    Returns:
        dict: Resultado da operação
    """
    os.makedirs(output_dir, exist_ok=True)

    resultados = run_csv_downloader(output_dir)

    logger.info("Iniciando conversão dos CSVs padronizados para JSON...")
    converter_csvs_para_json(output_dir)

    logger.info("Juntando JSONs por subopção...")
    juntar_jsons_por_opcao(output_dir)

    return resultados

if __name__ == "__main__":
    resultados = run_scraper()
    print(resultados)
