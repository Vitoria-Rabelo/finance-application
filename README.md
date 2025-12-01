# Finance Application (TP2)

API Financeira desenvolvida com FastAPI, SQLModel e Alembic.

## Como Rodar

1. Instale o uv: `pip install uv`
2. Instale as dependências: `uv sync`
3. Crie o arquivo `.env` e configure suas variáveis de ambiente
4. Gere o banco: `uv run alembic upgrade head`
5. Rode: `uv run uvicorn main:app --reload`

## Funcionalidades
- CRUD de Usuários, Contas, Categorias e Transações.
- Analytics e Balanço Financeiro.