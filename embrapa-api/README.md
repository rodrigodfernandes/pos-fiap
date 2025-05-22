# **FIAP-Embrapa API**

API REST desenvolvida para o projeto de pós-graduação em integração com a Embrapa. Esta API permite acesso a dados vitivinicultura, com recursos de autenticação, web scraping e comunicação com serviços externos.

## **📋 Índice**

* [Descrição](#bookmark=id.4gmmokdk7l07)

* [Tecnologias Utilizadas](#bookmark=id.fv9gogtct8um)

* [Arquitetura](#bookmark=id.5czf6ind3d4)

* [Requisitos](#bookmark=id.fgikzo2qc7g0)

* [Estrutura do Projeto](#bookmark=id.x3k52yf2evcj)

* [Instalação e Execução](#bookmark=id.ir1fehm9mmam)

* [Endpoints Disponíveis](#bookmark=id.vphvb3imasuw)

* [Stack de Monitoramento](#bookmark=id.n1bnlauuhgzs)

* [Desenvolvimento](#bookmark=id.1kwomqqwtmgq)

* [Utilizando Podman](#bookmark=id.epr832j4bg36)

* [Contribuição](#bookmark=id.tsaxplwwgcxh)

## **📝 Descrição**

Este projeto implementa uma API REST para coleta, processamento e disponibilização de dados relacionados a vitivinicultura da Embrapa. A aplicação possui funcionalidades de autenticação, acesso a banco de dados PostgreSQL, integração com APIs externas e capacidades de web scraping.

## **🔧 Tecnologias Utilizadas**

* **Backend**: Python 3.11 com FastAPI

* **Tarefas Assíncronas**: FastAPI BackgroundTasks

* **Banco de Dados**: PostgreSQL 16.8

* **Connection Pooling**: PgBouncer

* **Migrations**: Liquibase

* **Containerização**: Docker/Podman e Docker Compose/Podman Compose

* **Monitoramento**: Prometheus, Grafana, Loki

* **Documentação**: Swagger UI (integrado ao FastAPI)

## **🏗 Arquitetura**

A arquitetura do projeto segue os princípios de microserviços, com os seguintes componentes:

* **API Gateway**: Ponto de entrada para as requisições

* **Serviço de Autenticação**: Gerenciamento de usuários e autenticação

* **Serviço de Dados**: Acesso e manipulação dos dados da Embrapa

* **Web Scraping**: Coleta de dados de fontes externas

* **Banco de Dados**: Armazenamento persistente dos dados

* **Monitoramento**: Coleta e visualização de métricas e logs

## **📋 Requisitos**

* Docker e Docker Compose (ou Podman e Podman Compose como alternativas)

* Git

* Python 3.11+ (para desenvolvimento local)

## **📁 Estrutura do Projeto**

embrapa-api/  
├── .env \# Variáveis de ambiente  
├── .gitignore \# Arquivos a serem ignorados pelo git  
├── Dockerfile \# Configuração para build da imagem Docker  
├── docker-compose.yml \# Configuração dos serviços  
├── README.md \# Este documento  
├── requirements.txt \# Dependências Python  
├── monitoring/ \# Configurações de monitoramento │ ├── prometheus/ \# Configuração do Prometheus │ ├── grafana/ \# Configuração do Grafana │ ├── loki/ \# Configuração do Loki │ └── promtail/ \# Configuração do Promtail ├── migrations/ \# Diretório para migrações do Liquibase  
│ ├── local/  
│ │ └── init.sql \# Script SQL inicial para o banco de dados  
│ ├── changelog/ \# Arquivos de alteração do Liquibase  
│ │ └── db.changelog-master.xml  
│ └── liquibase.properties \# Configurações do Liquibase  
└── src/ \# Código fonte da aplicação  
├── \_\_init\_\_.py  
├── main.py \# Ponto de entrada da aplicação  
├── config/ \# Configurações da aplicação  
├── api/ \# Módulos da API  
│ ├── endpoints/ \# Endpoints da API │ │ ├── auth.py \# Autenticação │ │ ├── data.py \# Dados │ │ └── scraper.py \# Web scraping │ └── routes.py \# Configuração de rotas ├── core/ \# Lógica de negócios  
├── db/ \# Camada de acesso ao banco de dados  
├── scraper/ \# Módulo de web scraping  
│ └── embrapa\_scraper.py \# Implementação do scraper ├── tasks/ \# Tarefas assíncronas │ └── jobs.py \# Definição de jobs em background ├── external/ \# Integração com serviços externos  
└── utils/ \# Utilitários

## **🚀 Instalação e Execução**

### **Usando Docker (Recomendado)**

1. Clone o repositório:

git clone https://github.com/rodrigodfernandes/embrapa-api.git  
cd embrapa-api

2. Configure as variáveis de ambiente:

cp .env.example .env  
*\# Edite o arquivo .env conforme necessário*

3. Inicie os serviços com Docker Compose:

docker-compose up \-d

4. Verifique se os serviços estão funcionando:

docker-compose ps

### **Desenvolvimento Local**

1. Prepare o ambiente virtual Python:

python \-m venv venv  
source venv/bin/activate *\# No Windows use: venv\\Scripts\\activate*  
pip install \-r requirements.txt

2. Execute o banco de dados e serviços relacionados:

docker-compose up \-d embrapa-db pgbouncer embrapa-migrations

3. Execute a aplicação em modo de desenvolvimento:

uvicorn src.main:app \--reload \--host 0.0.0.0 \--port 8000

## **🔌 Endpoints Disponíveis**

A API possui os seguintes endpoints básicos:

* **Autenticação**: GET /api/auth \- Retorna o token da requisição após passar usuário e senha

* **Raiz da API**: GET / \- Retorna uma mensagem de boas-vindas

* **Verificação de Saúde**: GET /health \- Retorna o status da aplicação

* **Documentação Swagger**: GET /docs \- Interface interativa com a documentação da API

* **Documentação ReDoc**: GET /redoc \- Documentação alternativa da API

### **Endpoints de Scraping**

* **Execução Síncrona**: GET /api/scraper/executar \- Executa o scraping de forma síncrona

  * Parâmetros: output\_dir (opcional) \- Diretório onde os dados serão salvos

* **Execução Assíncrona**: POST /api/scraper/executar\_async \- Executa o scraping em background

  * Parâmetros:

    * output\_dir (opcional) \- Diretório onde os dados serão salvos

    * sleep\_time (opcional) \- Tempo de pausa entre operações (para controle de carga)

    * workers (opcional) \- Número de workers para paralelismo

* **Status da Tarefa**: GET /api/scraper/status/{task\_id} \- Verifica o status de uma tarefa assíncrona

  * Parâmetros: task\_id \- ID da tarefa retornado pela execução assíncrona

* **Listar Tarefas**: GET /api/scraper/tarefas \- Lista todas as tarefas de scraping

### **Endpoints Futuros**

* **Dados Agrícolas**: /api/data/\* \- Acesso aos dados coletados

* **Análises**: /api/analysis/\* \- Endpoints para análises específicas

## **📊 Stack de Monitoramento**

O projeto inclui uma stack completa de monitoramento com os seguintes componentes:

### **Prometheus (Métricas)**

* **Porta**: 9091

* **Função**: Coleta métricas de performance de todos os serviços

* **Acesso**: http://localhost:9091

### **Grafana (Visualização)**

* **Porta**: 3000

* **Função**: Dashboard para visualização de métricas e logs

* **Acesso**: http://localhost:3000

* **Credenciais Padrão**: admin/qwe123

* **Dashboard Principal**: Embrapa Monitoring

### **Loki (Logs)**

* **Porta**: 3102

* **Função**: Agregação e armazenamento de logs de todos os serviços

* **Integração**: Configurado como fonte de dados no Grafana

### **Exporters (Coletores de Métricas)**

* **postgres\_exporter**: Métricas do PostgreSQL

* **pgbouncer\_exporter**: Métricas do PgBouncer

* **node\_exporter**: Métricas do sistema host

* **container\_monitor**: Monitoramento personalizado de containers

### **Acessando o Monitoramento**

1. Acesse o Grafana em http://localhost:3000

2. Faça login com as credenciais padrão (admin/qwe123)

3. Navegue para o dashboard “Embrapa Monitoring” para visualizar:

   * Status dos serviços

   * Uso de recursos (CPU, memória)

   * Métricas de banco de dados

   * Logs de aplicação

## **💻 Desenvolvimento**

### **Autenticação**

**1\.** Como adicionar na função Para adicionar autenticação nas rotas criadas, basta adicionar **“current\_user: str \= Depends(get\_current\_user)”** na função que está dentro de endpoints, como no exemplo abaixo

@router.get("/protected")  
**def** protected(current\_user: str \= Depends(get\_current\_user)):  
  **return** {"message": f"Olá, {current\_user}. Você acessou uma rota protegida\!"}

**2\.** Como requisitar o token \* **2.1.** Chamar o endpoint de autenticação /api/auth passando usuário e senha, por fins de teste pode ser usado, eles são gravados critografados na base User: admin Password: mudar123

* **2.2.** A API de autenticação irá retornar um token, que deverá ser inserido na chamada da API que deseja utilizar, passando o token em Authorization / Bearer Token

### **Processamento Assíncrono**

O projeto utiliza o BackgroundTasks do FastAPI para execução assíncrona de tarefas pesadas, como o scraping de dados. Benefícios:

1. **Não bloqueia o servidor**: As requisições HTTP são respondidas imediatamente

2. **Paralelismo controlado**: É possível definir o número de workers

3. **Controle de carga**: O parâmetro sleep\_time permite pausas entre operações

4. **Rastreamento de progresso**: Endpoints para verificar o status e progresso das tarefas

### **Adicionando Novas Rotas**

Para adicionar novas rotas à API:

1. Crie um novo arquivo em src/api/endpoints/ para o recurso

2. Defina um router com os endpoints necessários

3. Importe e inclua o router em src/api/routes.py

Exemplo de um arquivo de endpoint src/api/endpoints/example.py:

**from** fastapi **import** APIRouter, HTTPException

router \= APIRouter()

@router.get(“/”)  
**async** **def** get\_examples():  
**return** {“examples”: \[“example1”, “example2”\]}

@router.get(“/{example\_id}”)  
**async** **def** get\_example(example\_id: int):  
**if** example\_id \< 1:  
**raise** HTTPException(status\_code=404, detail=“Example not found”)  
**return** {“example\_id”: example\_id, “name”: f”Example {example\_id}“}

Então, em src/api/routes.py:

**from** fastapi **import** APIRouter  
**from** src.api.endpoints **import** example, auth, data, scraper

router \= APIRouter()

router.include\_router(example.router, prefix=“/examples”, tags=\[“examples”\])  
router.include\_router(auth.router, prefix=“/auth”, tags=\[“authentication”\])  
router.include\_router(data.router, prefix=“/data”, tags=\[“data”\])  
router.include\_router(scraper.router, prefix=“/scraper”, tags=\[“scraping”\])

### **Banco de Dados**

O projeto utiliza PostgreSQL com connection pooling via PgBouncer. Para acessar o banco:

*\# Conectar diretamente ao PostgreSQL*  
docker-compose exec embrapa-db psql \-U postgres \-d fiap-embrapa

*\# Conectar via PgBouncer*  
docker-compose exec pgbouncer psql \-h localhost \-p 6432 \-U fiap-embrapa-app \-d fiap-embrapa

*\# Usando Podman*  
podman exec \-it embrapa-db psql \-U postgres \-d fiap-embrapa  
podman exec \-it pgbouncer psql \-h localhost \-p 6432 \-U fiap-embrapa-app \-d fiap-embrapa

## **🐳 Utilizando Podman**

Se preferir utilizar Podman em vez de Docker, você pode utilizar os seguintes comandos:

### **Iniciando com Podman Compose**

*\# Instalar Podman e Podman Compose (Ubuntu/Debian)*  
sudo apt-get update  
sudo apt-get install \-y podman  
pip3 install podman-compose

*\# Iniciar serviços*  
podman-compose up \-d

*\# Verificar status*  
podman-compose ps

*\# Logs*  
podman-compose logs \-f

*\# Parar serviços*  
podman-compose down

### **Comandos Podman Individuais**

*\# Criar rede*  
podman network create embrapa-net

*\# Executar banco de dados*  
podman run \-d \--name embrapa-db \\  
\--network embrapa-net \\  
\-p 5432:5432 \\  
\-e POSTGRES\_USER=postgres \\  
\-e POSTGRES\_PASSWORD=postgres \\  
\-e POSTGRES\_DB=fiap-embrapa \\  
\-v ./migrations/local/init.sql:/docker-entrypoint-initdb.d/init.sql \\  
postgres:16.8-alpine

*\# Executar PgBouncer*  
podman run \-d \--name pgbouncer \\  
\--network embrapa-net \\  
\-p 6432:6432 \\  
\-e POSTGRESQL\_USERNAME=fiap-embrapa-app \\  
\-e POSTGRESQL\_PASSWORD=fiap-embrapa-app \\  
\-e POSTGRESQL\_DATABASE=fiap-embrapa \\  
\-e PGBOUNCER\_DATABASE=fiap-embrapa \\  
\-e PGBOUNCER\_POOL\_MODE=transaction \\  
\-e PGBOUNCER\_IGNORE\_STARTUP\_PARAMETERS=extra\_float\_digits \\  
\-e POSTGRESQL\_HOST=embrapa-db \\  
bitnami/pgbouncer

*\# Executar aplicação*  
podman build \-t embrapa-api .  
podman run \-d \--name embrapa-api \\  
\--network embrapa-net \\  
\-p 8000:8000 \\  
\-e DB\_HOST=pgbouncer \\  
\-e DB\_PORT=6432 \\  
\-e DB\_USER=fiap-embrapa-app \\  
\-e DB\_PASSWORD=fiap-embrapa-app \\  
\-e DB\_NAME=fiap-embrapa \\  
\-v ./src:/app/src \\  
embrapa-api

Para informações mais detalhadas sobre o uso do Podman, consulte o arquivo PODMAN\_GUIDE.md incluído neste projeto.

## **👥 Contribuição**

Para contribuir com o projeto:

1. Faça um fork do repositório

2. Crie uma branch para sua feature (git checkout \-b feature/nova-funcionalidade)

3. Commit suas mudanças (git commit \-am ‘Adiciona nova funcionalidade’)

4. Push para a branch (git push origin feature/nova-funcionalidade)

5. Crie um Pull Request

---

Desenvolvido para o projeto de pós-graduação FIAP.