import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.api.endpoints.auth import router
from src.models.user import User
from src.core.auth.schemas import UserLogin
from src.config.database import SessionLocal
from fastapi import FastAPI

# Mock dependencies
@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)

@pytest.fixture
def mock_db_session():
    db = MagicMock()
    yield db

@pytest.fixture
def mock_user():
    user = User(username="testuser", password="$2b$12$KIXQ8l1E6y6h1Q9Q9Q9Q9u")  # bcrypt hash for "password"
    return user

def test_login_success(client, mock_user, monkeypatch):
    # Mock do banco de dados
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_db.query.return_value = mock_query

    # Substitui o SessionLocal pelo mock
    monkeypatch.setattr("src.api.endpoints.auth.SessionLocal", lambda: mock_db)

    # Mock da verificação de senha
    monkeypatch.setattr("src.api.endpoints.auth.pwd_context.verify", lambda pw, hashed: pw == "password")

    # Mock da criação do token
    monkeypatch.setattr("src.api.endpoints.auth.create_access_token", lambda identity: "mocked_token")

    # Faz a requisição ao endpoint
    response = client.post("/login", json={"username": "testuser", "password": "password"})

    # Verifica os resultados
    assert response.status_code == 200
    assert response.json() == {"access_token": "mocked_token", "token_type": "bearer"}
def test_login_invalid_credentials(client, monkeypatch):
    # Mock do banco de dados
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None  # Nenhum usuário encontrado
    mock_db.query.return_value = mock_query

    # Substitui o SessionLocal pelo mock
    monkeypatch.setattr("src.api.endpoints.auth.SessionLocal", lambda: mock_db)

    # Faz a requisição ao endpoint
    response = client.post("/login", json={"username": "wronguser", "password": "wrongpassword"})

    # Verifica os resultados
    assert response.status_code == 400
    assert response.json() == {"detail": "Credenciais inválidas"}