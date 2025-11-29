from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User
from app.models.transaction import Transaction

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    tipo: str
    saldo_inicial: float
    usuario_id: int = Field(foreign_key="User.id")
    usuario: "User" = Relationship(back_populates="accounts")
    transactions: list["Transaction"] = Relationship(back_populates="conta")

Account.model_rebuild()

