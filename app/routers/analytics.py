from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func, col
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User, Category, Transaction, Account

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

# ==========================================
# 1. Search (Busca na Descrição)
# ==========================================
@router.get("/transactions/search", response_model=List[Transaction])
async def search_transactions(
    q: str,
    session: AsyncSession = Depends(get_session),
):
    if not q:
        return []
        
    pattern = f"%{q}%"
    # Busca case-insensitive
    query = select(Transaction).where(col(Transaction.descricao).ilike(pattern))
    result = await session.execute(query)
    return result.scalars().all()


# ==========================================
# 2. Count Total Transactions
# ==========================================
@router.get("/transactions/count")
async def count_transactions(
    session: AsyncSession = Depends(get_session),
):
    query = select(func.count(Transaction.id))
    result = await session.execute(query)
    total = result.scalar()
    return {"total_transactions": total or 0}


# ==========================================
# 3. Count by Category (Agregação)
# ==========================================
@router.get("/transactions/count-by-category")
async def count_transactions_by_category(
    session: AsyncSession = Depends(get_session),
):
    query = (
        select(Category.nome, func.count(Transaction.id))
        .join(Transaction, Transaction.categoria_id == Category.id, isouter=True)
        .group_by(Category.nome)
    )
    result = await session.execute(query)
    rows = result.all()
    
    return [
        {"category": row[0], "count": row[1]} 
        for row in rows
    ]


# ==========================================
# 4. Transactions per User (Agregação)
# ==========================================
@router.get("/users/transactions-count")
async def count_transactions_per_user(
    session: AsyncSession = Depends(get_session),
):
    query = (
        select(User.nome, func.count(Transaction.id))
        .join(Account, Account.usuario_id == User.id, isouter=True)
        .join(Transaction, Transaction.conta_id == Account.id, isouter=True)
        .group_by(User.nome)
    )
    result = await session.execute(query)
    rows = result.all()
    
    return [
        {"user": row[0], "count": row[1]} 
        for row in rows
    ]


# ==========================================
# 5. Balanço Geral (Receitas vs Despesas) - NOVO 🚀
# ==========================================
@router.get("/balance-summary")
async def get_balance_summary(
    session: AsyncSession = Depends(get_session),
):
    """
    Retorna o total de Receitas, Total de Despesas e o Saldo Líquido.
    """
    # 1. Calcular Total de Receitas
    query_receitas = select(func.sum(Transaction.valor)).where(
        col(Transaction.tipo).ilike("Receita") # ilike para garantir (receita/Receita)
    )
    result_receitas = await session.execute(query_receitas)
    total_receitas = result_receitas.scalar() or 0.0

    # 2. Calcular Total de Despesas
    query_despesas = select(func.sum(Transaction.valor)).where(
        col(Transaction.tipo).ilike("Despesa")
    )
    result_despesas = await session.execute(query_despesas)
    total_despesas = result_despesas.scalar() or 0.0

    # 3. Calcular Saldo
    saldo = total_receitas - total_despesas

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo_liquido": saldo,
        "status": "No Azul" if saldo >= 0 else "No Vermelho"
    }

# ==========================================
# Outros Endpoints Úteis (IDs, Ano, etc)
# ==========================================

@router.get("/transactions/by-year/{year}", response_model=List[Transaction])
async def list_transactions_by_year(
    year: int,
    session: AsyncSession = Depends(get_session),
):
    query = select(Transaction).where(
        func.strftime("%Y", Transaction.data) == str(year)
    )
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.id == user_id).options(selectinload(User.accounts), selectinload(User.categories))
    result = await session.execute(query)
    user = result.scalars().first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction_by_id(transaction_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Transaction).where(Transaction.id == transaction_id).options(selectinload(Transaction.conta), selectinload(Transaction.categoria))
    result = await session.execute(query)
    transaction = result.scalars().first()
    if not transaction: raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction