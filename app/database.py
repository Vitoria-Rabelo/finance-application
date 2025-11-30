from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("configure novamente suas variáveis no arquivo .env")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# Session maker
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# Dependência para FastAPI
async def get_session():
    async with SessionLocal() as session:
        yield session


# CREATE ALL opcional
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
