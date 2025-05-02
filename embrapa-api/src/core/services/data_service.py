import json
from pathlib import Path
from sqlalchemy.engine import Connection
from sqlalchemy import text

MODULE_TABLES = {
    "product": "product",
    # "process": "process",
    # "sales": "sales",
    # "import": "import",
    # "export": "export",
}

def insert_all_data(conn: Connection):
    for module, table_name in MODULE_TABLES.items():
        # @TODO: Alterar para usar o caminho correto do arquivo JSON
        json_file_path = Path(f"src/scraper/{module}.json")
        if not json_file_path.exists():
            raise FileNotFoundError(f"JSON file for module '{module}' not found at {json_file_path}.")

        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"Invalid data format in {json_file_path}. Expected a list of objects.")

        for record in data:
            if not isinstance(record, dict):
                raise ValueError(f"Invalid record format in {json_file_path}. Each record must be a dictionary.")

            columns = ", ".join(record.keys())
            values = ", ".join([f":{key}" for key in record.keys()])
            query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            print(f"Executing query: {query} with values: {record}")
            
            try:
                conn.execute(query, record)
            except Exception as e:
                raise RuntimeError(f"Failed to insert record into {table_name}: {e}")
            
            conn.commit()

def get_data_by_module(module: str, conn: Connection):
    if module not in MODULE_TABLES:
        raise ValueError(f"Invalid module '{module}'. Valid modules are: {', '.join(MODULE_TABLES.keys())}.")

    query = text(f"SELECT * FROM {MODULE_TABLES[module]}")
    result = conn.execute(query)
    
    return [dict(row._mapping) for row in result]