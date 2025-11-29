from sqlmodel import SQLModel, Field, Relationship
from app.models.category import Category
from app.models.account import Account
from datetime import datetime, timezone

class Transaction(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    descricao: str
    valor: float
    data: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tipo: str
    conta_id: int = Field(foreign_key=True)
    categoria_id: int | None = Field(default=None, foreign_key="category.id")

    conta: "Account" = Relationship(back_populates="transactions")
    categoria: "Category" = Relationship(back_populates="transactions")

Transaction.model_rebuild()

