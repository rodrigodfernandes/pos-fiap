FROM python:3.11-slim

WORKDIR /app

# Criar diretórios para dados
RUN mkdir -p /app/data/vitibrasil

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY ./src /app/src

# Garantir permissões de escrita no diretório de dados
RUN chmod -R 777 /app/data

# Comando para iniciar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
