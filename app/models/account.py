from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    tipo: str
    saldo_inicial: float
    usuario_id: int | None = Field(default=None, foreign_key="user.id")

    usuario: Optional["User"] = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="conta")


# --- Schemas ---

class AccountBase(SQLModel):
    nome: str
    tipo: str
    saldo_inicial: float
    usuario_id: int

class AccountCreate(AccountBase):
    pass

class AccountRead(AccountBase):
    id: int

class AccountUpdate(SQLModel):
    nome: str | None = None
    tipo: str | None = None
    saldo_inicial: float | None = None
