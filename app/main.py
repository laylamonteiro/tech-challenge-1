# app/main.py

import asyncio
from contextlib import asynccontextmanager
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from app import auth
from app.auth import user_dependency
from app.db import create_db_and_tables, get_session
from app.routers import comercio, exportacao, importacao, processamento, producao
from etl.ingestion_df import db_ingestion

app = FastAPI(
    title="Tech Challenge 1 API",
    version="1.0.0",
    description="<b>Alunos</b>:<br><br>Bruno Enrico: <b>RM363607</b> <br>Douglas Fernando: <b>RM362545</b> <br> Gabrielle Bellini: <b>RM362017</b> <br>Layla Monteiro: <b>RM364476</b> <br>Tamiris Lira: <b>RM362467</b>",
)

# Contexto de inicialização (se necessário criar BD/tabelas, por exemplo)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se você precisar rodar algo antes de startup, faça aqui.
    # Ex.: create_db_and_tables(), db_ingestion(), etc.
    create_db_and_tables()
    yield
    # Cleanup (se necessário) após shutdown
    # ...

app.router.lifespan_context = lifespan

# Inclui o módulo de autenticação (se tiver endpoints de auth)
app.include_router(auth.router)

# Todas as demais rotas ficam sob o prefixo /api
app.include_router(processamento.router, prefix="/api")
app.include_router(comercio.router, prefix="/api")
app.include_router(exportacao.router, prefix="/api")
app.include_router(importacao.router, prefix="/api")
app.include_router(producao.router, prefix="/api")

# Se você quiser uma rota raiz simples, por exemplo:
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    # Redireciona diretamente para /docs (Swagger UI)
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


# **************************************************
# ** IMPORTANTE: se você quiser que QUALQUER rota **
# ** diferente seja redirecionada para /docs,        **
# ** você pode usar um middleware “catch‐all” aqui. **
# **************************************************
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Exemplo de “catch‐all” para rotas inexistentes: 
@app.middleware("http")
async def catch_all_redirect(request: Request, call_next):
    response = await call_next(request)
    # Se for 404 e não tiver sido tratada por nenhuma rota, redireciona para /docs
    if response.status_code == 404:
        return RedirectResponse(url="/docs")
    return response

# Se você quiser rodar localmente com uvicorn por uma linha de comando, mantenha o bloco abaixo:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
