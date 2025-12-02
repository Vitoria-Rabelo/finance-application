import asyncio
import random
from datetime import datetime, timedelta

from sqlmodel import select
from app.database import SessionLocal
from app.models.user import User
from app.models.category import Category
from app.models.account import Account
from app.models.transaction import Transaction

async def seed():
    print("Iniciando seed expandido...")
    
    async with SessionLocal() as session:
        # Verifica se já tem dados para não duplicar
        result = await session.exec(select(User))
        if result.first():
            print("Banco já possui dados. Apague o arquivo .db se quiser resetar.")
            return

        print("--- Gerando 10 Categorias ---")
        # Lista de tuplas (Nome, Tipo)
        cat_data = [
            ("Alimentação", "DESPESA"),
            ("Transporte", "DESPESA"),
            ("Moradia", "DESPESA"),
            ("Saúde", "DESPESA"),
            ("Educação", "DESPESA"),
            ("Lazer", "DESPESA"),
            ("Vestuário", "DESPESA"),
            ("Salário", "RECEITA"),
            ("Investimentos", "RECEITA"),
            ("Freelance", "RECEITA"),
        ]
        
        categories = []
        for nome, tipo in cat_data:
            categories.append(Category(nome=nome, tipo=tipo))
        
        session.add_all(categories)
        await session.flush() # Para gerar os IDs

        print("--- Gerando 10 Usuários ---")
        user_names = [
            "Ana Silva", "Bruno Costa", "Carlos Lima", "Diana Prince", 
            "Eduardo Rocha", "Fernanda Souza", "Gabriel Medina", 
            "Helena Troy", "Igor Santos", "Julia Roberts"
        ]
        
        users = []
        for i, name in enumerate(user_names):
            # Cria emails unicos baseados no nome
            email = f"{name.split()[0].lower()}{i}@example.com"
            users.append(User(nome=name, email=email, senha_hash=f"hash_{i}"))
            
        session.add_all(users)
        await session.flush()

        print("--- Gerando 10 Contas (1 por usuário) ---")
        acc_types = ["Corrente", "Poupança", "Investimento", "Carteira", "Digital"]
        bank_names = ["Nubank", "Inter", "Itaú", "Bradesco", "Binance"]
        
        accounts = []
        for i, user in enumerate(users):
            # Escolhe um tipo e banco aleatório para variar
            acc_type = acc_types[i % len(acc_types)] 
            bank_name = bank_names[i % len(bank_names)]
            
            accounts.append(Account(
                nome=f"{bank_name} - {acc_type}",
                tipo=acc_type,
                saldo_inicial=random.randint(100, 5000) * 1.0, # Saldo entre 100 e 5000
                usuario_id=user.id
            ))
            
        session.add_all(accounts)
        await session.flush()

        print("--- Gerando 10 Transações ---")
        transactions = []
        descriptions = [
            "Compra no Mercado", "Gasolina", "Cinema", "Aluguel", 
            "Farmácia", "Livros", "Jantar", "Recebimento Salário", 
            "Venda de Ações", "Projeto Extra"
        ]

        for i in range(10):
            # Escolhe aleatoriamente uma conta e uma categoria existentes
            random_acc = random.choice(accounts)
            random_cat = random.choice(categories)
            
            # Define o tipo da transação baseado na categoria escolhida
            tipo_transacao = random_cat.tipo 
            
            # Gera uma data aleatória nos últimos 60 dias
            days_ago = random.randint(0, 60)
            date_trans = datetime.now() - timedelta(days=days_ago)

            transactions.append(Transaction(
                descricao=descriptions[i],
                valor=random.randint(50, 1000) * 1.0, # Valor aleatório
                data=date_trans,
                tipo=tipo_transacao,
                conta_id=random_acc.id,
                categoria_id=random_cat.id
            ))

        session.add_all(transactions)
        
        await session.commit()
        print("Seed finalizado! 10 de cada entidade criados com sucesso.")

if __name__ == "__main__":
    asyncio.run(seed())