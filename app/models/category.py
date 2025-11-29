from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User
from app.models.transaction import Transaction

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    tipo: str
    usuario_id: int = Field(foreign_key="User.id")

Category.model_rebuild()

usuario: "User" = Relationship(back_populates="categories")
transactions: list["Transaction"] = Relationship(back_populates="categories")
