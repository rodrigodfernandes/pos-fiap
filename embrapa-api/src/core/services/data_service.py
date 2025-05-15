import json
from pathlib import Path
from sqlalchemy.engine import Connection
from sqlalchemy import text
from src.db.models import Product, Process, Sales, Import, Export
DATA_PATH = Path("../../../data/vitibrasil")

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

def insert_all_data(conn: Connection):
    """
    Inserts data from all JSON files into the database.
    """
    for module, file_name in MODULE_TABLES.items():
        json_file_path = Path(f"{DATA_PATH}/{file_name}.json")
        print(json_file_path)
        if not json_file_path.exists():
            raise FileNotFoundError(f"JSON file for module '{module}' not found at {json_file_path}.")

        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"Invalid data format in {json_file_path}. Expected a list of objects.")

        # Obter o modelo correspondente ao módulo
        model = MODEL_MAPPING[module]
        mapping = model.json_to_db_mapping

        # Inserir cada registro no banco de dados
        for record in data:
            if not isinstance(record, dict):
                raise ValueError(f"Invalid record format in {json_file_path}. Each record must be a dictionary.")

            # Converter os dados do JSON para o formato esperado pelo banco de dados
            db_record = {mapping[key]: value for key, value in record.items() if key in mapping}

            # Remover valores inválidos (ex.: "-")
            db_record = {k: (None if v == "-" else v) for k, v in db_record.items()}

            columns = ", ".join(db_record.keys())
            values = ", ".join([f":{key}" for key in db_record.keys()])
            query = text(f"INSERT INTO {module} ({columns}) VALUES ({values})")
            
            try:
                conn.execute(query, db_record)
            except Exception as e:
                raise RuntimeError(f"Failed to insert record into {module}: {e}")

    conn.commit()

def get_data_by_module(module: str, conn: Connection):
    if module not in MODULE_TABLES:
        raise ValueError(f"Invalid module '{module}'. Valid modules are: {', '.join(MODULE_TABLES.keys())}.")

    query = text(f"SELECT * FROM product")
    result = conn.execute(query)
    
    return [dict(row._mapping) for row in result]