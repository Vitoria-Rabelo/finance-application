from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.database import get_session
from app.models import Account, AccountCreate, AccountRead, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["Contas"])

@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(conta: AccountCreate, session: AsyncSession = Depends(get_session)):
    db_account = Account.model_validate(conta)
    session.add(db_account)
    await session.commit()
    await session.refresh(db_account)
    return db_account

@router.get("/", response_model=list[AccountRead])
async def read_accounts(session: AsyncSession = Depends(get_session)):
    query = select(Account).options(
        joinedload(Account.usuario)
    )
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/{account_id}", response_model=AccountRead)
async def read_account(account_id: int, session: AsyncSession = Depends(get_session)):
    account = await session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account

@router.delete("/{account_id}")
async def delete_account(account_id: int, session: AsyncSession = Depends(get_session)):
    account = await session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    await session.delete(account)
    await session.commit()
    return {"ok": True}