from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .links import UserCategoryLink 

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction

class CategoryBase(SQLModel):
    nome: str
    tipo: str

class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    users: List["User"] = Relationship(back_populates="categories", link_model=UserCategoryLink)
    
    transactions: List["Transaction"] = Relationship(back_populates="categoria")

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

class CategoryUpdate(SQLModel):
    nome: str | None = None
    tipo: str | None = None