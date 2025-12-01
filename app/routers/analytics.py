from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session  # AJUSTE conforme seu projeto
from app.models.user import User      # AJUSTE caminhos
from app.models.category import Category
from app.models.transaction import Transaction

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

# a) Consultas por ID (User e Transaction)

@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.transactions),
            selectinload(User.categories),
        )
    )
    user = result.first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction_by_id(
    transaction_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(Transaction)
        .where(Transaction.id == transaction_id)
        .options(
            selectinload(Transaction.user),
            selectinload(Transaction.category),
        )
    )
    transaction = result.first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transaction


# b) Listar todas as transações de um determinado usuário

@router.get("/users/{user_id}/transactions", response_model=List[Transaction])
async def list_transactions_by_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .options(selectinload(Transaction.category))
    )
    return result.all()


# c) Listar todos os usuários de uma determinada categoria (N:N)

@router.get("/categories/{category_id}/users", response_model=List[User])
async def list_users_by_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(User)
        .join(User.categories)
        .where(Category.id == category_id)
        .options(selectinload(User.categories))
    )
    return result.all()


# d) Listar transações de determinado ano

@router.get("/transactions/by-year/{year}", response_model=List[Transaction])
async def list_transactions_by_year(
    year: int,
    session: AsyncSession = Depends(get_session),
):
    # Para SQLite: func.strftime
    result = await session.exec(
        select(Transaction).where(
            func.strftime("%Y", Transaction.date) == str(year)
        )
    )
    return result.all()


# e) Busca por texto parcial na descrição

@router.get("/transactions/search", response_model=List[Transaction])
async def search_transactions(
    q: str,
    session: AsyncSession = Depends(get_session),
):
    pattern = f"%{q}%"
    result = await session.exec(
        select(Transaction).where(Transaction.description.ilike(pattern))
    )
    return result.all()


# f) Exemplo: usuários criados em determinado ano (ou troque por outro campo de data)

@router.get("/users/by-year/{year}", response_model=List[User])
async def list_users_by_year(
    year: int,
    session: AsyncSession = Depends(get_session),
):
    # Ajuste o campo de data conforme o seu modelo (created_at, birth_date, etc.)
    result = await session.exec(
        select(User).where(
            func.strftime("%Y", User.created_at) == str(year)
        )
    )
    return result.all()


# g) Quantidade total de transações

@router.get("/transactions/count")
async def count_transactions(
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(func.count(Transaction.id)))
    total = result.one()
    return {"total_transactions": total}


# h) Quantidade de transações por categoria

@router.get("/transactions/count-by-category")
async def count_transactions_by_category(
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(Category.name, func.count(Transaction.id))
        .join(Transaction, Transaction.category_id == Category.id, isouter=True)
        .group_by(Category.id, Category.name)
        .order_by(Category.name)
    )
    rows = result.all()
    return [
        {"category": name, "total_transactions": count}
        for name, count in rows
    ]


# i) Quantidade de transações por usuário

@router.get("/users/transactions-count")
async def count_transactions_per_user(
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(User.id, User.name, func.count(Transaction.id))
        .join(Transaction, Transaction.user_id == User.id, isouter=True)
        .group_by(User.id, User.name)
        .order_by(User.name)
    )
    rows = result.all()
    return [
        {
            "user_id": user_id,
            "user_name": name,
            "transactions": count,
        }
        for user_id, name, count in rows
    ]


# j) Transações com valor (amount) acima de certo mínimo

@router.get("/transactions/min-value/{value}", response_model=List[Transaction])
async def list_transactions_above_value(
    value: float,
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(Transaction).where(Transaction.amount >= value)
    )
    return result.all()
