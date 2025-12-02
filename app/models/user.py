from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .links import UserCategoryLink

if TYPE_CHECKING:
    from .account import Account
    from .category import Category


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str

    accounts: List["Account"] = Relationship(back_populates="usuario")
    categories: List["Category"] = Relationship(back_populates="users", link_model=UserCategoryLink)


# --- Schemas (Pydantic) para a API ---

class UserBase(SQLModel):
    nome: str
    email: str

class UserCreate(UserBase):
    senha: str  # Senha em texto puro para criar

class UserRead(UserBase):
    id: int
    # Não retornamos a senha aqui por segurança

class UserUpdate(SQLModel):
    nome: str | None = None
    email: str | None = None
    senha: str | None = None