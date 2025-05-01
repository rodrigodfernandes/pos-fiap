from fastapi import APIRouter
from src.config.database import SessionLocal
from passlib.context import CryptContext
from src.api.endpoints.auth import router as auth_router

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função utilitária para acesso ao DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login e geração de token
router.include_router(auth_router, prefix="/auth", tags=["auth"])
