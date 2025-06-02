import asyncio
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, select
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from app import auth
from app.auth import get_current_user
from app.db import create_db_and_tables, get_session, engine
from app.model.tables import User
from app.routers import comercio, exportacao, importacao, processamento, producao
from etl.ingestion_df import db_ingestion

# Contexto para hash de senha (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define o FastAPI (inclua title/description se quiser)
app = FastAPI(
    title="Tech Challenge 1 API",
    version="1.0.0",
    description="<b>Alunos</b>:<br><br>Bruno Enrico: <b>RM363607</b> <br>Douglas Fernando: <b>RM362545</b> <br> Gabrielle Bellini: <b>RM362017</b> <br>Layla Monteiro: <b>RM364476</b> <br>Tamiris Lira: <b>RM362467</b> <br><br> admin:<b>admin</b>",
)

# =========================================================================================
# 1) Adicione esta seção inteira para criar o usuário padrão “admin” no SQLite ao iniciar.
# =========================================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1.1) Cria as tabelas (caso ainda não existam)
    create_db_and_tables()

    # 1.2) Garante que exista um usuário “admin” com senha “admin”
    with Session(engine) as session:
        default_username = "admin"
        default_password = "admin"

        # Verifica se já existe
        statement = select(User).where(User.username == default_username)
        existing_user = session.exec(statement).first()
        if not existing_user:
            # Se não existir, cria e faz commit
            hashed_pw = pwd_context.hash(default_password)
            user_obj = User(username=default_username, hashed_password=hashed_pw)
            session.add(user_obj)
            session.commit()
            print(f"🔐 Usuário padrão '{default_username}' criado com senha '{default_password}'.")

    # 1.3) Agora chame seu ETL normal (db_ingestion)
    db_ingestion()

    yield  # fim do startup; agora a aplicação entra em modo "pronta para receber requisições"

    # (Opcional) Se quiser rodar algo no shutdown, coloque aqui
    # print("Shutdown tasks...")

# Conecta o lifespan ao FastAPI
app.router.lifespan_context = lifespan

# =========================================================================================
# 2) Rotas de autenticação e dependência de usuário logado (já devem existir em auth.py)
# =========================================================================================
app.include_router(auth.router)  # Isso inclui: POST /login, etc.

# =========================================================================================
# 3) Suas rotas de negócio (prefixo /api)
# =========================================================================================
app.include_router(processamento.router, prefix="/api")
app.include_router(comercio.router, prefix="/api")
app.include_router(exportacao.router, prefix="/api")
app.include_router(importacao.router, prefix="/api")
app.include_router(producao.router, prefix="/api")

# =========================================================================================
# 4) Middleware “catch-all” para redirecionar 404 → /docs (Swagger UI)
# =========================================================================================
@app.middleware("http")
async def catch_all_redirect(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        return RedirectResponse(url="/docs")
    return response

# =========================================================================================
# 5) Execução local via uvicorn (opcional)
# =========================================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
