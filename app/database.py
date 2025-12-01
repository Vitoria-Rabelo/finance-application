from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import event
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
from pathlib import Path
import os

# 1. Configuração do Caminho e .env
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("configure novamente suas variáveis no arquivo .env")

# 2. Configuração Dinâmica dos Argumentos (O Pulo do Gato)
connect_args = {}

# Se for SQLite, não precisa de SSL (dá erro se passar).
# Se for Postgres (Supabase/Neon), geralmente precisa de SSL.
if "sqlite" not in DATABASE_URL:
    connect_args["ssl"] = "require"

# 3. Criação da Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False, # Mude para True se quiser ver o SQL no terminal
    future=True,
    connect_args=connect_args, # Injeta os argumentos calculados acima
)

# 4. FIX Obrigatório para SQLite: Ativar Foreign Keys
# Sem isso, o SQLite deixa você salvar uma Transação com conta_id=999 mesmo se a conta 999 não existir.
if "sqlite" in DATABASE_URL:
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# 5. Session Maker
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# 6. Dependência para FastAPI
async def get_session():
    async with SessionLocal() as session:
        yield session

# 7. Init DB (Opcional/Dev)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)