from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descricao: str
    valor: float
    data: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tipo: str
    conta_id: int | None = Field(default=None, foreign_key="account.id")
    categoria_id: int | None = Field(default=None, foreign_key="category.id")

    conta: "Account" | None = Relationship(back_populates="transactions")
    categoria: "Category" | None = Relationship(back_populates="transactions")