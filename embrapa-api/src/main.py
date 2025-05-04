import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router
from prometheus_fastapi_instrumentator import Instrumentator

# Garantir que os diretórios necessários existam
os.makedirs("data/vitibrasil", exist_ok=True)


app = FastAPI(
    title="Embrapa API",
    description="API REST para o projeto de pós-graduação FIAP-Embrapa",
    version="0.1.0"
)

# Initialize and expose metrics
Instrumentator().instrument(app).expose(app)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "FIAP-Embrapa API"}

# @app.get("/health")
# async def health_check():
#     return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

