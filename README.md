# Finance Application (TP2)

API Financeira desenvolvida com FastAPI, SQLModel e Alembic.

## Como Rodar

1. Instale o uv: `pip install uv`
2. Instale as dependências: `uv sync`
3. Selecione seu banco de dados no `.env`
4. Gere o banco: `uv run alembic upgrade head`
5. Rode: `uv run uvicorn main:app --reload`
6. Povoe o banco executando o seed com `python seed.py`
5. Suba a aplicação denovo com: `uv run uvicorn main:app --reload`

## Funcionalidades
- CRUD de Usuários, Contas, Categorias e Transações.
- Analytics e Balanço Financeiro.