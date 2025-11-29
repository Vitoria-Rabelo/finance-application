# app/database/database.py

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import event

# 1) Carrega o .env da raiz do projeto
BASE_DIR = Path(__file__).resolve().parents[2]  # .../finance-application
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

# 2) Lê a URL do banco (aqui o tipo já é str, não str|None)
DATABASE_URL: str = os.environ["DATABASE_URL"]

# 3) Configurações específicas por tipo de banco
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # Postgres/Neon
    connect_args = {"ssl": "require"}

# 4) Engine assíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,                # log das queries
    connect_args=connect_args
)

# 5) Session async
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 6) Dependency injection para FastAPI
async def get_session():
    async with SessionLocal() as session:
        yield session

# 7) Criar tabelas (somente aqui, não na main)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# 8) Ativar foreign_keys apenas para SQLite
if DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine.sync_engine, "connect")
    def activate_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
