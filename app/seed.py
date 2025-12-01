from datetime import date
import asyncio

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import SessionLocal  # usa a SessionLocal já configurada
from app.models.user import User      # ajuste o caminho se seus modelos estiverem em outro lugar
from app.models.category import Category
from app.models.transaction import Transaction


async def seed():
    # Abre uma sessão assíncrona usando a SessionLocal do seu database.py
    async with SessionLocal() as session:  # SessionLocal já é async_sessionmaker(...)
        # Verifica se já existe algum usuário para não duplicar seed
        result = await session.exec(select(User))
        if result.first():
            print("Banco já possui dados. Seed não executado.")
            return

            # ==== CATEGORIAS ====
        categories = [
            Category(nome="Alimentação", tipo="DESPESA"),
            Category(nome="Transporte", tipo="DESPESA"),
            Category(nome="Educação", tipo="DESPESA"),
            Category(nome="Lazer", tipo="DESPESA"),
            Category(nome="Saúde", tipo="DESPESA"),
        ]
        session.add_all(categories)
        await session.flush()  # garante que categories terão IDs

        # ==== USUÁRIOS ====
        users = [
            User(nome="Ana Silva", email="ana@example.com", senha_hash="hash_teste_1"),
            User(nome="Bruno Costa", email="bruno@example.com", senha_hash="hash_teste_2"),
            User(nome="Carla Lima", email="carla@example.com", senha_hash="hash_teste_3"),
        ]
        session.add_all(users)
        await session.flush()   


       # ==== TRANSAÇÕES (pelo menos 10 instâncias) ====
        transactions = [
            Transaction(
                descricao="Supermercado",
                valor=250.0,
                data=date(2024, 1, 10),
                tipo="DESPESA",
                conta_id=1,  # ajuste conforme sua tabela de contas
                categoria_id=categories[0].id,
            ),
            Transaction(
                descricao="Uber",
                valor=35.0,
                data=date(2024, 1, 11),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[1].id,
            ),
            Transaction(
                descricao="Plano de saúde",
                valor=450.0,
                data=date(2024, 2, 3),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[4].id,
            ),
            Transaction(
                descricao="Cinema",
                valor=50.0,
                data=date(2024, 2, 15),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[3].id,
            ),
            Transaction(
                descricao="Curso de Python",
                valor=399.0,
                data=date(2024, 3, 1),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[2].id,
            ),
            Transaction(
                descricao="Combustível",
                valor=180.0,
                data=date(2024, 3, 10),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[1].id,
            ),
            Transaction(
                descricao="Restaurante",
                valor=120.5,
                data=date(2024, 4, 5),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[0].id,
            ),
            Transaction(
                descricao="Livros",
                valor=220.0,
                data=date(2024, 4, 18),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[2].id,
            ),
            Transaction(
                descricao="Consulta médica",
                valor=300.0,
                data=date(2024, 5, 2),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[4].id,
            ),
            Transaction(
                descricao="Show",
                valor=350.0,
                data=date(2024, 6, 20),
                tipo="DESPESA",
                conta_id=1,
                categoria_id=categories[3].id,
            ),
        ]


        session.add_all(transactions)

        # Se você tiver tabela de associação UserCategory (N:N) e quiser popular aqui,
        # crie e adicione os objetos de link também.

        await session.commit()
        print("Seed executado com sucesso.")


if __name__ == "__main__":
    asyncio.run(seed())
