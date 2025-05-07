from sqlalchemy import Column, Integer, String
from src.config.database import Base

# Modelo de usuário
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # hash da senha
