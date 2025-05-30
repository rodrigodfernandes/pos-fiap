from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.auth.auth_handler import get_jwt_identity

# Extrair o token do cabeçalho Authorization e injetar na variavel token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Recupera o usuário atual via token
def get_current_user(token: str = Depends(oauth2_scheme)):
    identity = get_jwt_identity(token)
    if not identity:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autorizado")
    return identity
