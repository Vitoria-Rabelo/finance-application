from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Transforma UserCreate (senha pura) em User (banco)
    # OBS: Num mundo real, criptografaríamos a senha aqui.
    db_user = User(nome=user.nome, email=user.email, senha_hash=user.senha)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserRead])
async def read_users(session: AsyncSession = Depends(get_session)):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()