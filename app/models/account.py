from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    tipo: str
    saldo_inicial: float
    usuario_id: int | None = Field(default=None, foreign_key="user.id")

    usuario: "User" | None = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="conta")

