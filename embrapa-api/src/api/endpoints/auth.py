from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.auth.auth_bearer import get_current_user
from src.core.auth.auth_handler import create_access_token
from src.models.user import User
from passlib.context import CryptContext
from src.config.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm

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
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = create_access_token(identity=str(user.username))
    return {"access_token": token, "token_type": "bearer"}