from sqlmodel import SQLModel, Field

class UserCategoryLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    category_id: int | None = Field(default=None, foreign_key="category.id", primary_key=True)