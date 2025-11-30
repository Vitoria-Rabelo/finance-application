from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str

    accounts: list["Account"] = Relationship(back_populates="usuario")
    categories: list["Category"] = Relationship(back_populates="usuario")
