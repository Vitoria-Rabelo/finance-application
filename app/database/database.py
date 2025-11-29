from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv, find_dotenv
import logging
import os

# Load .env reliably by finding it in the project tree
env_path = find_dotenv()
if not env_path:
    logging.warning(".env not found with find_dotenv(); ensure .env is in project root or set env vars externally")
else:
    load_dotenv(env_path)

# configuracoes do log
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise RuntimeError("DATABASE_URL not set. Check your .env or environment variables")

engine = create_async_engine(DB_URL)

# create an async session factory
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_session() -> AsyncSession:
    """Return a new AsyncSession instance from the session factory.

    Use as `async with get_session() as session:` or integrate as a FastAPI dependency.
    """
    return async_session()