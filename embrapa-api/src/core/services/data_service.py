import json
from pathlib import Path
from sqlalchemy.engine import Connection
from sqlalchemy import text
from src.db.models import ColorEnum, GrapeTypeEnum, KindEnum, WineDerivativeEnum
from src.db.repositories.data_repository import (
    delete_product_data,
    delete_process_data,
    delete_sales_data,
    delete_import_data,
    delete_export_data,
    get_all_from_table,
    insert_into_product,
    insert_into_process,
    insert_into_sales,
    insert_into_import,
    insert_into_export
)

DATA_PATH = "data/vitibrasil"

MODULE_FILES = {
    "product": "opt_02_completo",
    "process": "opt_03_completo",
    "sales": "opt_04_completo",
    "import": "opt_05_completo",
    "export": "opt_06_completo",
}

def load_data(module: str):
    file_name = MODULE_FILES[module]
    json_file_path = Path(f"{DATA_PATH}/{file_name}.json")
    if not json_file_path.exists():
        raise FileNotFoundError(f"JSON não encontrado em {json_file_path}.")
    with open(json_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def insert_product_data(conn: Connection):
    delete_product_data(conn)

    data = load_data("product")
    current_wine_derivative = None
    insertions = []

    for entry in data:
        produto = entry.get("Produto", "").strip()
        quantidade_raw = entry.get("Quantidade (L.)", "0").replace(".", "").replace("-", "0")

        if produto == "Total":
            continue

        try:
            quantidade = int(float(quantidade_raw))
        except ValueError:
            quantidade = 0

        if produto.isupper():
            current_wine_derivative = produto

        if current_wine_derivative is None:
            continue # ignorar registros antes do primeiro UPPERCASE

        insertions.append({
            "name": produto,
            "wine_derivative_name": current_wine_derivative,
            "quantity": quantidade
        })

    for record in insertions:
        try:
            insert_into_product(conn, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir produto {record}: {e}")

    conn.commit()

def insert_process_data(conn: Connection):
    delete_process_data(conn)

    data = load_data("process")
    current_color_name = None
    insertions = []
    valid_kinds = [e.value for e in KindEnum]
    valid_colors = [e.value for e in ColorEnum]

    for entry in data:
        cultivar = entry.get("Cultivar", "").strip()
        quantidade_raw = entry.get("Quantidade (Kg)", "0").replace(".", "").replace(",", ".").replace("-", "0")
        kind_raw = entry.get("type", "").strip()

        if cultivar == "Total":
            continue

        try:
            quantidade = int(float(quantidade_raw))
        except ValueError:
            quantidade = 0

        if cultivar.isupper() and cultivar in valid_colors:
            current_color_name = cultivar

        if current_color_name is None or not kind_raw:
            continue

        if kind_raw not in valid_kinds:
            raise ValueError(f"Tipo inválido encontrado: '{kind_raw}'")

        insertions.append({
            "color_name": current_color_name,
            "kind_name": kind_raw,
            "cultivar": cultivar,
            "quantity_kg": quantidade
        })

    for record in insertions:
        try:
            insert_into_process(conn, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir processamento {record}: {e}")

    conn.commit()

def insert_sales_data(conn: Connection):
    delete_sales_data(conn)

    data = load_data("sales")
    current_wine_derivative = None
    insertions = []
    valid_wine_derivatives = [e.value for e in WineDerivativeEnum]

    for entry in data:
        produto = entry.get("Produto", "").strip()
        quantidade_raw = entry.get("Quantidade (L.)", "0").replace(".", "").replace("-", "0")

        if produto == "Total":
            continue

        try:
            quantidade = int(float(quantidade_raw))
        except ValueError:
            quantidade = 0

        if produto.isupper() and produto in valid_wine_derivatives:
            current_wine_derivative = produto

        if current_wine_derivative is None:
            continue

        insertions.append({
            "name": produto,
            "wine_derivative_name": current_wine_derivative,
            "quantity_liters": quantidade
        })

    for record in insertions:
        try:
            insert_into_sales(conn, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir comercialização {record}: {e}")

    conn.commit()

def insert_import_data(conn: Connection):
    delete_import_data(conn)

    data = load_data("import")
    insertions = []
    valid_grape_types = [e.value for e in GrapeTypeEnum]

    for entry in data:
        country = entry.get("Países", "").strip()
        quantidade_raw = entry.get("Quantidade (Kg)", "0").replace(".", "").replace("-", "0")
        valor_raw = entry.get("Valor (US$)", "0").replace(".", "").replace("-", "0").replace(",", ".")
        grape_type = entry.get("type", "").strip()

        if country == "Total":
            continue

        try:
            quantidade = int(float(quantidade_raw))
        except ValueError:
            quantidade = 0

        try:
            valor = float(valor_raw)
        except ValueError:
            valor = 0.0

        if not grape_type or grape_type not in valid_grape_types:
            continue

        insertions.append({
            "grape_type_name": grape_type,
            "country": country,
            "quantity_kg": quantidade,
            "value_usd": valor
        })

    for record in insertions:
        try:
            insert_into_import(conn, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir importação {record}: {e}")

    conn.commit()

def insert_export_data(conn: Connection):
    delete_export_data(conn)

    data = load_data("export")
    insertions = []
    valid_grape_types = [e.value for e in GrapeTypeEnum]

    for entry in data:
        country = entry.get("Países", "").strip()
        quantidade_raw = entry.get("Quantidade (Kg)", "0").replace(".", "").replace("-", "0")
        valor_raw = entry.get("Valor (US$)", "0").replace(".", "").replace("-", "0").replace(",", ".")
        grape_type = entry.get("type", "").strip()

        if country == "Total":
            continue

        try:
            quantidade = int(float(quantidade_raw))
        except ValueError:
            quantidade = 0

        try:
            valor = float(valor_raw)
        except ValueError:
            valor = 0.0

        if not grape_type or grape_type not in valid_grape_types:
            continue

        insertions.append({
            "grape_type_name": grape_type,
            "country": country,
            "quantity_kg": quantidade,
            "value_usd": valor
        })

    for record in insertions:
        try:
            insert_into_export(conn, record)
        except Exception as e:
            raise RuntimeError(f"Erro ao inserir exportação {record}: {e}")

    conn.commit()

def insert_all_data(conn: Connection):
    insert_product_data(conn)
    insert_process_data(conn)
    insert_sales_data(conn)
    insert_import_data(conn)
    insert_export_data(conn)

def get_data_by_module(module: str, conn: Connection):
    if module not in MODULE_FILES:
        raise ValueError(f"Invalid module '{module}'. Valid modules are: {', '.join(MODULE_FILES.keys())}.")

    result = get_all_from_table(module, conn)
    return result
