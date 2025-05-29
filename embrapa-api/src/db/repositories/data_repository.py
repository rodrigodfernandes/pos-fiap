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

def get_all_from_table(table: str, conn: Connection, year_no: int = None, skip: int = 0, limit: int = 100):
    base_query = f"SELECT * FROM {table}"
    params = {}

    if year_no is not None:
        base_query += " WHERE year_no = :year_no"
        params["year_no"] = year_no

    base_query += " ORDER BY id OFFSET :skip LIMIT :limit"
    params.update({"skip": skip, "limit": limit})

    query = text(base_query)
    result = conn.execute(query, params)
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