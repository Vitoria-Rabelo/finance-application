from sqlmodel import SQLModel, Field, Relationship
from app.models.account import Account 
from app.models.category import Category
class User(SQLModel, table=True):
    
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True, index=True)
    senha_hash: str
    accounts: list["Account"] = Relationship(back_populates="users")
    categories: list["Category"] = Relationship(back_populates="users")
    
User.model_rebuild()
