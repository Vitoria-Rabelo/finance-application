from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import Category, CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categorias"])

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(categoria: CategoryCreate, session: AsyncSession = Depends(get_session)):
    db_category = Category.model_validate(categoria)
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category

@router.get("/", response_model=list[CategoryRead])
async def read_categories(session: AsyncSession = Depends(get_session)):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(category_id: int, categoria_data: CategoryUpdate, session: AsyncSession = Depends(get_session)):
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    hero_data = categoria_data.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_category, key, value)
        
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(category_id: int, session: AsyncSession = Depends(get_session)):
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    await session.delete(category)
    await session.commit()
    return {"ok": True}