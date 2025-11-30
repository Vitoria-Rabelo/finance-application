from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import (
    Transaction, TransactionCreate, TransactionRead, TransactionUpdate,
    Account, Category
)

router = APIRouter(prefix="/transactions", tags=["Transações"])

@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(transacao: TransactionCreate, session: AsyncSession = Depends(get_session)):
    db_transacao = Transaction.model_validate(transacao)
    session.add(db_transacao)
    await session.commit()
    await session.refresh(db_transacao)
    return db_transacao

@router.get("/", response_model=list[TransactionRead])
async def read_transactions(session: AsyncSession = Depends(get_session)):
    # Aqui usamos o JOINEDLOAD como o professor pediu
    query = select(Transaction).options(
        joinedload(Transaction.conta),
        joinedload(Transaction.categoria)
    )
    result = await session.execute(query)
    return result.scalars().all()

@router.delete("/{id}")
async def delete_transaction(id: int, session: AsyncSession = Depends(get_session)):
    transacao = await session.get(Transaction, id)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    await session.delete(transacao)
    await session.commit()
    return {"ok": True}