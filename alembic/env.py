from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env early so we can set or override alembic config.url
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não encontrado no .env")


from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ensure alembic has a sqlalchemy.url set (use .env DATABASE_URL if present)
if not config.get_main_option("sqlalchemy.url") and DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel

# Import application models so SQLModel.metadata is populated for autogenerate
try:
    import app.models  # this module should import each model submodule
except Exception:
    # if imports fail, continue — autogenerate may still work if metadata is set elsewhere
    pass

# Now set the target metadata from SQLModel after models are imported
from sqlmodel import SQLModel
target_metadata = SQLModel.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode'."""

    from sqlalchemy.ext.asyncio import create_async_engine

    url = config.get_main_option("sqlalchemy.url") or DATABASE_URL
    if url is None:
        raise RuntimeError("No database URL configured for Alembic (sqlalchemy.url or .env DATABASE_URL)")

    # Engine async com SSL habilitado (necessário para Neon)
    async_engine = create_async_engine(
        url,
        poolclass=pool.NullPool,
        connect_args={"ssl": True},
    )

    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    import asyncio

    async def run_async_migrations():
        async with async_engine.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())



    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    import asyncio

    async def run_async_migrations():
        async with async_engine.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
