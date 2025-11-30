from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    tipo: str
    usuario_id: int | None = Field(default=None, foreign_key="user.id")

    usuario: "User" | None = Relationship(back_populates="categories")
    transactions: list["Transaction"] = Relationship(back_populates="categoria")
