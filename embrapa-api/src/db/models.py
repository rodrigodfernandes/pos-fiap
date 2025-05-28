import enum
from sqlalchemy import Column, Integer, String, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# @TODO: melhorar e utilizar o mapping

# region Enums
class ColorEnum(enum.Enum):
    TINTA = 'TINTAS'
    BRANCAS_E_ROSADAS = 'BRANCAS E ROSADAS'

class KindEnum(enum.Enum):
    VINIFERAS = 'Viníferas'
    AMERICANAS_E_HIBRIDAS = 'Americanas e híbridas'
    UVAS_DE_MESA = 'Uvas de mesa'
    SEM_CLASSIFICACAO = 'Sem classificação'
    PRINCIPAL = 'principal'

class WineDerivativeEnum(enum.Enum):
    VINHO_DE_MESA = 'VINHO DE MESA'
    VINHO_FINO_DE_MESA = 'VINHO FINO DE MESA'
    VINHO_FRIZANTE = 'VINHO FRIZANTE'
    VINHO_ORGANICO = 'VINHO ORGÂNICO'
    VINHO_ESPECIAL = 'VINHO ESPECIAL'
    ESPUMANTES = 'ESPUMANTES'
    SUCO = 'SUCO'
    SUCO_DE_UVAS = 'SUCO DE UVAS'
    SUCO_DE_UVAS_CONCENTRADO = 'SUCO DE UVAS CONCENTRADO'
    DERIVADOS = 'DERIVADOS'
    OUTROS = 'OUTROS PRODUTOS COMERCIALIZADOS'

class GrapeTypeEnum(enum.Enum):
    VINHOS_DE_MESA = 'Vinhos de mesa'
    ESPUMANTES = 'Espumantes'
    UVAS_FRESCAS = 'Uvas frescas'
    UVAS_PASSAS = 'Uvas passas'
    SUCO_DE_UVA = 'Suco de uva'
# endregion

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    wine_derivative_name = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

class Process(Base):
    __tablename__ = "process"
    id = Column(Integer, primary_key=True, index=True)
    color_name = Column(Enum(ColorEnum), nullable=False)
    kind_name = Column(Enum(KindEnum), nullable=False)      # por enquanto apenas tipo Vinifera
    cultivar = Column(String(100), nullable=False)
    quantity_kg = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    wine_derivative_name = Column(Enum(WineDerivativeEnum), nullable=False)
    quantity_liters = Column(Numeric(15, 2), nullable=False)
    year = Column(Integer, nullable=False)

class Import(Base):
    __tablename__ = "import"
    id = Column(Integer, primary_key=True, index=True)
    grape_type_name = Column(Enum(GrapeTypeEnum), nullable=False)        # por enquanto apenas tipo Vinhos de mesa
    country = Column(String(100), nullable=False)
    quantity_kg = Column(Numeric(15, 2))
    value_usd = Column(Numeric(15, 2))
    year = Column(Integer, nullable=False)

class Export(Base):
    __tablename__ = "export"
    id = Column(Integer, primary_key=True, index=True)
    grape_type_name = Column(Enum(GrapeTypeEnum), nullable=False)        # por enquanto apenas tipo Vinhos de mesa
    country = Column(String(100), nullable=False)
    quantity_kg = Column(Numeric(15, 2))
    value_usd = Column(Numeric(15, 2))
    year = Column(Integer, nullable=False)
