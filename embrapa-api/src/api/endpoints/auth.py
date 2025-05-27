from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.auth.auth_bearer import get_current_user
from src.core.auth.auth_handler import create_access_token
from src.core.auth.schemas import UserLogin
from src.models.user import User
from passlib.context import CryptContext
from src.config.database import SessionLocal

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Login e geração de token
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    API para autenticação de usuário e geração de token JWT.
    - **data**: Objeto UserLogin contendo username e password.
    - Retorna um token JWT se as credenciais forem válidas.
    """
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    token = create_access_token(identity=str(user.username))
    return {"access_token": token, "token_type": "bearer"}