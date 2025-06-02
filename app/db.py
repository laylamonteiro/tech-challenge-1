from sqlmodel import SQLModel, create_engine, Session
import os

# Por padrão (sem var de ambiente), uso SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Se for SQLite, precisa desse argumento para uso multithread
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
