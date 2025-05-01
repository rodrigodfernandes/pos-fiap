from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "chave-super-secreta"  # Mude para algo mais seguro em produção
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração do token

# Função para criar o token
def create_access_token(identity: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": identity,  # 'sub' é a identidade do usuário
        "exp": expire     # Expiração do token
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Função para validar o token e recuperar a identidade
def get_jwt_identity(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Retorna a identidade (username ou user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token inválido")
