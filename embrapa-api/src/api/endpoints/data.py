from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.engine import Connection
from src.config.database import get_db
from src.core.services.data_service import insert_all_data, get_data_by_module
from src.core.auth.auth_bearer import get_current_user

router = APIRouter()

@router.post("/import-all")
def import_all_data(db: Connection = Depends(get_db), _: str = Depends(get_current_user)):
    try:
        insert_all_data(db)
        return {"message": "All data imported successfully."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/product")
def get_product_data(
    ano: int = Query(None, description="Filtrar os dados pelo ano de referência"),
    pagina: int = Query(
        default=1,
        ge=1,
        title="Página",
        description="Número da página (começando em 1)"
    ),
    qtd_por_pagina: int = Query(
        default=100,
        ge=1,
        title="Quantidade por página",
        description="Número de itens por página"
    ),
    db: Connection = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        skip = (pagina - 1) * qtd_por_pagina
        data = get_data_by_module("product", db, year_no=ano, skip=skip, limit=qtd_por_pagina)
        return {
            "modulo": "product",
            "pagina": pagina,
            "quantidade_por_pagina": qtd_por_pagina,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/process")
def get_process_data(
    ano: int = Query(None, description="Filtrar os dados pelo ano de referência"),
    pagina: int = Query(
        default=1,
        ge=1,
        title="Página",
        description="Número da página (começando em 1)"
    ),
    qtd_por_pagina: int = Query(
        default=100,
        ge=1,
        title="Quantidade por página",
        description="Número de itens por página"
    ),
    db: Connection = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        skip = (pagina - 1) * qtd_por_pagina
        data = get_data_by_module("process", db, year_no=ano, skip=skip, limit=qtd_por_pagina)
        return {
            "modulo": "process",
            "pagina": pagina,
            "quantidade_por_pagina": qtd_por_pagina,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/sales")
def get_sales_data(
    ano: int = Query(None, description="Filtrar os dados pelo ano de referência"),
    pagina: int = Query(
        default=1,
        ge=1,
        title="Página",
        description="Número da página (começando em 1)"
    ),
    qtd_por_pagina: int = Query(
        default=100,
        ge=1,
        title="Quantidade por página",
        description="Número de itens por página"
    ),
    db: Connection = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        skip = (pagina - 1) * qtd_por_pagina
        data = get_data_by_module("sales", db, year_no=ano, skip=skip, limit=qtd_por_pagina)
        return {
            "modulo": "sales",
            "pagina": pagina,
            "quantidade_por_pagina": qtd_por_pagina,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/import")
def get_import_data(
    ano: int = Query(None, description="Filtrar os dados pelo ano de referência"),
    pagina: int = Query(
        default=1,
        ge=1,
        title="Página",
        description="Número da página (começando em 1)"
    ),
    qtd_por_pagina: int = Query(
        default=100,
        ge=1,
        title="Quantidade por página",
        description="Número de itens por página"
    ),
    db: Connection = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        skip = (pagina - 1) * qtd_por_pagina
        data = get_data_by_module("import", db, year_no=ano, skip=skip, limit=qtd_por_pagina)
        return {
            "modulo": "import",
            "pagina": pagina,
            "quantidade_por_pagina": qtd_por_pagina,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/export")
def get_export_data(
    ano: int = Query(None, description="Filtrar os dados pelo ano de referência"),
    pagina: int = Query(
        default=1,
        ge=1,
        title="Página",
        description="Número da página (começando em 1)"
    ),
    qtd_por_pagina: int = Query(
        default=100,
        ge=1,
        title="Quantidade por página",
        description="Número de itens por página"
    ),
    db: Connection = Depends(get_db),
    _: str = Depends(get_current_user)
):
    try:
        skip = (pagina - 1) * qtd_por_pagina
        data = get_data_by_module("export", db, year_no=ano, skip=skip, limit=qtd_por_pagina)
        return {
            "modulo": "export",
            "pagina": pagina,
            "quantidade_por_pagina": qtd_por_pagina,
            "dados": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")