import json
from pathlib import Path
from sqlalchemy.engine import Connection
from sqlalchemy import text
from src.db.models import GrapeTypeEnum, KindEnum, Product, Process, Sales, Import, Export
DATA_PATH = "data/vitibrasil"

# @TODO: deixar mais genérico, com menos hardcode nos métodos, usando o mapping...
MODULE_TABLES = {
    "product": "opt_02",
    "process": "opt_03",
    "sales": "opt_04",
    "import": "opt_05",
    "export": "opt_06",
}

MODEL_MAPPING = {
    "product": Product,
    "process": Process,
    "sales": Sales,
    "import": Import,
    "export": Export
}

def insert_product_data(conn: Connection):
    # se já tiver conteúdo na tabela, apaga tudo antes de inserir
    conn.execute(text("DELETE FROM product;"))
    conn.commit()
    
    json_file_path = Path(f"{DATA_PATH}/opt_02.json")
    if not json_file_path.exists():
        raise FileNotFoundError(f"JSON file not found at {json_file_path}.")

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    current_wine_derivative = None
    insertions = []

    for entry in data:
        produto = entry.get("Produto", "").strip()
        quantidade_raw = entry.get("Quantidade (L.)", "0").replace(".", "").replace("-", "0")
        
        if produto == "Total":
            continue

        try:
            quantidade = quantidade_raw
        except ValueError:
            quantidade = 0

        if produto.isupper():
            current_wine_derivative = produto

        if current_wine_derivative is None:
            continue  # ignorar registros antes do primeiro UPPERCASE

        insertions.append({
            "name": produto,
            "wine_derivative_name": current_wine_derivative,
            "quantity": quantidade
        })

    for record in insertions:
        query = text("""
            INSERT INTO product (name, wine_derivative_name, quantity)
            VALUES (:name, :wine_derivative_name, :quantity)
        """)
        try:
            conn.execute(query, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir produto {record}: {e}")

    conn.commit()

def insert_process_data(conn: Connection):
    conn.execute(text("DELETE FROM process;"))
    conn.commit()

    json_file_path = Path(f"{DATA_PATH}/opt_03.json")
    if not json_file_path.exists():
        raise FileNotFoundError(f"JSON file not found at {json_file_path}.")

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    current_color_name = None
    insertions = []

    for entry in data:
        cultivar = entry.get("Cultivar", "").strip()
        quantidade_raw = entry.get("Quantidade (Kg)", "0").replace(".", "").replace("-", "0")

        if cultivar == "Total":
            continue

        try:
            quantidade = quantidade_raw
        except ValueError:
            quantidade = 0

        if cultivar.isupper():
            current_color_name = cultivar

        if current_color_name is None:
            continue

        insertions.append({
            "color_name": current_color_name,
            "kind_name": KindEnum.VINIFERAS.value,
            "cultivar": cultivar,
            "quantity_kg": quantidade
        })

    for record in insertions:
        query = text("""
            INSERT INTO process (color_name, kind_name, cultivar, quantity_kg)
            VALUES (:color_name, :kind_name, :cultivar, :quantity_kg)
        """)
        try:
            conn.execute(query, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir processamento {record}: {e}")

    conn.commit()

def insert_sales_data(conn: Connection):
    conn.execute(text("DELETE FROM sales;"))
    conn.commit()

    json_file_path = Path(f"{DATA_PATH}/opt_04.json")
    if not json_file_path.exists():
        raise FileNotFoundError(f"JSON file not found at {json_file_path}.")

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    current_wine_derivative = None
    insertions = []

    for entry in data:
        produto = entry.get("Produto", "").strip()
        quantidade_raw = entry.get("Quantidade (L.)", "0").replace(".", "").replace("-", "0")

        if produto == "Total":
            continue

        try:
            quantidade = quantidade_raw
        except ValueError:
            quantidade = 0

        if produto.isupper():
            current_wine_derivative = produto

        if current_wine_derivative is None:
            continue

        insertions.append({
            "name": produto,
            "wine_derivative_name": current_wine_derivative,
            "quantity_liters": quantidade
        })

    for record in insertions:
        query = text("""
            INSERT INTO sales (name, wine_derivative_name, quantity_liters)
            VALUES (:name, :wine_derivative_name, :quantity_liters)
        """)
        try:
            conn.execute(query, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir comercialização {record}: {e}")

    conn.commit()

def insert_import_data(conn: Connection):
    conn.execute(text("DELETE FROM import;"))
    conn.commit()

    json_file_path = Path(f"{DATA_PATH}/opt_05.json")
    if not json_file_path.exists():
        raise FileNotFoundError(f"JSON file not found at {json_file_path}.")

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    insertions = []

    for entry in data:
        country = entry.get("Países", "").strip()
        quantidade_raw = entry.get("Quantidade (Kg)", "0").replace(".", "").replace("-", "0")
        valor_raw = entry.get("Valor (US$)", "0").replace(".", "").replace("-", "0").replace(",", ".")

        if country == "Total":
            continue

        try:
            quantidade = quantidade_raw
        except ValueError:
            quantidade = 0

        try:
            valor = float(valor_raw)
        except ValueError:
            valor = 0.0

        insertions.append({
            "grape_type_name": GrapeTypeEnum.VINHOS_DE_MESA.value,
            "country": country,
            "quantity_kg": quantidade,
            "value_usd": valor
        })

    for record in insertions:
        query = text("""
            INSERT INTO import (grape_type_name, country, quantity_kg, value_usd)
            VALUES (:grape_type_name, :country, :quantity_kg, :value_usd)
        """)
        try:
            conn.execute(query, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir importação {record}: {e}")

    conn.commit()

def insert_export_data(conn: Connection):
    conn.execute(text("DELETE FROM export;"))
    conn.commit()

    json_file_path = Path(f"{DATA_PATH}/opt_06.json")
    if not json_file_path.exists():
        raise FileNotFoundError(f"JSON file not found at {json_file_path}.")

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    insertions = []

    for entry in data:
        country = entry.get("Países", "").strip()
        quantidade_raw = entry.get("Quantidade (Kg)", "0").replace(".", "").replace("-", "0")
        valor_raw = entry.get("Valor (US$)", "0").replace(".", "").replace("-", "0").replace(",", ".")

        if country == "Total":
            continue

        try:
            quantidade = quantidade_raw
        except ValueError:
            quantidade = 0

        try:
            valor = float(valor_raw)
        except ValueError:
            valor = 0.0

        insertions.append({
            "grape_type_name": GrapeTypeEnum.VINHOS_DE_MESA.value,
            "country": country,
            "quantity_kg": quantidade,
            "value_usd": valor
        })

    for record in insertions:
        query = text("""
            INSERT INTO export (grape_type_name, country, quantity_kg, value_usd)
            VALUES (:grape_type_name, :country, :quantity_kg, :value_usd)
        """)
        try:
            conn.execute(query, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir exportação {record}: {e}")

    conn.commit()

def insert_all_data(conn: Connection):
    """
    Inserts data from all JSON files into the database.
    """
    insert_product_data(conn)
    insert_process_data(conn)
    insert_sales_data(conn)
    insert_import_data(conn)
    insert_export_data(conn)
    

def get_data_by_module(module: str, conn: Connection):
    if module not in MODULE_TABLES:
        raise ValueError(f"Invalid module '{module}'. Valid modules are: {', '.join(MODULE_TABLES.keys())}.")

    query = text(f"SELECT * FROM {module};")
    result = conn.execute(query)
    
    return [dict(row._mapping) for row in result]