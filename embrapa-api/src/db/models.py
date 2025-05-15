from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Mapeamento JSON -> Banco de Dados
    json_to_db_mapping = {
        "Produto": "name",
        "Quantidade (L.)": "quantity"
    }

class Process(Base):
    __tablename__ = "process"
    id = Column(Integer, primary_key=True, autoincrement=True)
    color_id = Column(Integer, ForeignKey("color.id"))
    kind_id = Column(Integer, ForeignKey("kind.id"))
    cultivar = Column(String(100), nullable=False)
    quantity_kg = Column(Integer, nullable=False)

    json_to_db_mapping = {
        "Cultivar": "cultivar",
        "Quantidade (Kg)": "quantity_kg"
    }

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    wine_type_id = Column(Integer, ForeignKey("wine_derivative_type.id"))
    quantity_liters = Column(Numeric(15, 2), nullable=False)

    json_to_db_mapping = {
        "Produto": "wine_type_id",  # Ajuste conforme necessário
        "Quantidade (L.)": "quantity_liters"
    }

class Import(Base):
    __tablename__ = "import"
    id = Column(Integer, primary_key=True, autoincrement=True)
    grape_type_id = Column(Integer, ForeignKey("grape_type.id"))
    country = Column(String(100), nullable=False)
    quantity_kg = Column(Numeric(15, 2))
    value_usd = Column(Numeric(15, 2))

    json_to_db_mapping = {
        "Países": "country",
        "Quantidade (Kg)": "quantity_kg",
        "Valor (US$)": "value_usd"
    }

class Export(Base):
    __tablename__ = "export"
    id = Column(Integer, primary_key=True, autoincrement=True)
    grape_type_id = Column(Integer, ForeignKey("grape_type.id"))
    country = Column(String(100), nullable=False)
    quantity_kg = Column(Numeric(15, 2))
    value_usd = Column(Numeric(15, 2))

    json_to_db_mapping = {
        "Países": "country",
        "Quantidade (Kg)": "quantity_kg",
        "Valor (US$)": "value_usd"
    }