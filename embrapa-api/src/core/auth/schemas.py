# app/auth/schemas.py
from pydantic import BaseModel

# Modelo de dados para autenticação
class UserLogin(BaseModel):
    username: str
    password: str