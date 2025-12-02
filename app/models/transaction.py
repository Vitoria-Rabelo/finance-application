from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .account import Account, AccountRead
    from .category import Category, CategoryRead

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descricao: str
    valor: float
    data: datetime = Field(default_factory=datetime.now)
    tipo: str
    conta_id: int | None = Field(default=None, foreign_key="account.id")
    categoria_id: int | None = Field(default=None, foreign_key="category.id")

    conta: Optional["Account"] = Relationship(back_populates="transactions")
    categoria: Optional["Category"] = Relationship(back_populates="transactions")


# --- Schemas ---
class TransactionBase(SQLModel):
    descricao: str
    valor: float
    tipo: str
    conta_id: int
    categoria_id: int
    # Data é opcional pois já tem default factory no modelo

class TransactionCreate(TransactionBase):
    data: datetime | None = None 

class TransactionRead(TransactionBase):
    id: int
    data: datetime
    
    conta: Optional["AccountRead"] = None
    categoria: Optional["CategoryRead"] = None

class TransactionUpdate(SQLModel):
    descricao: str | None = None
    valor: float | None = None
    tipo: str | None = None
    data: datetime | None = None
    
    
from .account import AccountRead
from .category import CategoryRead
TransactionRead.model_rebuild()