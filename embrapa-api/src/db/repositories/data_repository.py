from sqlalchemy.engine import Connection
from sqlalchemy import text

def insert_into_product(conn: Connection, record: dict):
    query = text("""
        INSERT INTO product (name, wine_derivative_name, quantity, year_no)
        VALUES (:name, :wine_derivative_name, :quantity, :year_no)
    """)
    conn.execute(query, record)

def insert_into_process(conn: Connection, record: dict):
    query = text("""
        INSERT INTO process (color_name, kind_name, cultivar, quantity_kg, year_no)
        VALUES (:color_name, :kind_name, :cultivar, :quantity_kg, :year_no)
    """)
    conn.execute(query, record)

def insert_into_sales(conn: Connection, record: dict):
    query = text("""
        INSERT INTO sales (name, wine_derivative_name, quantity_liters, year_no)
        VALUES (:name, :wine_derivative_name, :quantity_liters, :year_no)
    """)
    conn.execute(query, record)

def insert_into_import(conn: Connection, record: dict):
    query = text("""
        INSERT INTO import (grape_type_name, country, quantity_kg, value_usd, year_no)
        VALUES (:grape_type_name, :country, :quantity_kg, :value_usd, :year_no)
    """)
    conn.execute(query, record)

def insert_into_export(conn: Connection, record: dict):
    query = text("""
        INSERT INTO export (grape_type_name, country, quantity_kg, value_usd, year_no)
        VALUES (:grape_type_name, :country, :quantity_kg, :value_usd, :year_no)
    """)
    conn.execute(query, record)

def delete_all_from_table(table: str, conn: Connection):
    conn.execute(text(f"DELETE FROM {table};"))
    conn.commit()

def get_all_from_table(table: str, conn: Connection, year_no: int = None):
    if year_no is not None:
        query = text(f"SELECT * FROM {table} WHERE year_no = :year_no;")
        result = conn.execute(query, {"year_no": year_no})
    else:
        query = text(f"SELECT * FROM {table};")
        result = conn.execute(query)
    return [dict(row._mapping) for row in result]

def delete_product_data(conn: Connection):
    delete_all_from_table("product", conn)

def delete_process_data(conn: Connection):
    delete_all_from_table("process", conn)

def delete_sales_data(conn: Connection):
    delete_all_from_table("sales", conn)

def delete_import_data(conn: Connection):
    delete_all_from_table("import", conn)

def delete_export_data(conn: Connection):
    delete_all_from_table("export", conn)

def get_product_data(conn: Connection):
    return get_all_from_table("product", conn)

def get_process_data(conn: Connection):
    return get_all_from_table("process", conn)

def get_sales_data(conn: Connection):
    return get_all_from_table("sales", conn)

def get_import_data(conn: Connection):
    return get_all_from_table("import", conn)

def get_export_data(conn: Connection):
    return get_all_from_table("export", conn)