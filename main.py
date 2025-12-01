from fastapi import FastAPI
from app.routers import users, transactions
from app.routers import accounts, categories, analytics

app = FastAPI(title="Finance Application - TP2")

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(analytics.router) 

@app.get("/")
def health_check():
    return {
        "status": "API rodando com sucesso!",
        "docs": "Acesse /docs para ver o Swagger"
    }