# BIBLIOTECAS

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# DADOS DO PROJETO

vendedores = ["Ana", "Bruno", "Carla", "Diego"]
salarios = {"Ana":1500, "Bruno":1400, "Carla":1450, "Diego":1500}

products = [
    ("P001", "Notebook Lenovo", 3500),
    ("P002", "Mouse Sem Fio", 50),
    ("P003", "Teclado Mecânico", 250),
    ("P004", "Monitor 24", 900),
    ("P005", "Fone Gamer", 180),
]

metodos_pagamento = ["dinheiro", "pix", "cartao_credito"]

inicio = datetime(2024, 1, 1)
fim    = datetime(2025, 12, 31)

dias = (fim - inicio).days + 1

# GERAR DADOS 

dados = []
sale_id = 1

for i in range(dias):
    data = inicio + timedelta(days=i)

    vendas_do_dia = np.random.randint(2, 12)  # 2 a 12 vendas por dia

    for _ in range(vendas_do_dia):
        produto = products[np.random.randint(len(products))]
        vendedor = vendedores[np.random.randint(len(vendedores))]
        qtd = np.random.randint(1, 4)
        metodo = np.random.choice(metodos_pagamento)

        # DESCONTO

        if metodo in ["dinheiro", "pix"]:
            desconto_pct = round(np.random.uniform(0, 10), 2)
        else:
            desconto_pct = round(np.random.uniform(0, 15), 2)

        desconto_valor = (produto[2] * qtd) * (desconto_pct / 100)
        total = (produto[2] * qtd) - desconto_valor

        dados.append([
            sale_id,
            data.strftime("%Y-%m-%d"),
            produto[0],
            qtd,
            produto[2],
            desconto_pct,
            round(desconto_valor, 2),
            round(total, 2),
            metodo,
            vendedor
        ])
        sale_id += 1

cols = [
    "sale_id", "date", "product_code", "quantity", "unit_price",
    "discount_pct", "discount_value", "total", "payment_type", "seller_name"
]

df = pd.DataFrame(dados, columns=cols)

#SALVAR CSV

df.to_csv("sales_sample.csv", index=False)
print("Arquivo CSV criado!")

# BANCO DE DADOS SQLITE

conn = sqlite3.connect("loja_vendas.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("DROP TABLE IF EXISTS sellers")
cursor.execute("DROP TABLE IF EXISTS products")

cursor.execute("""
    CREATE TABLE products (
        code TEXT PRIMARY KEY,
        description TEXT,
        price REAL
    )
""")

cursor.executemany("INSERT INTO products VALUES (?, ?, ?)", products)

cursor.execute("""
    CREATE TABLE sellers (
        seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        base_salary REAL
    )
""")
cursor.executemany("INSERT INTO sellers (name, base_salary) VALUES (?, ?)",
                   [(v, salarios[v]) for v in vendedores])

cursor.execute("""
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        date TEXT,
        product_code TEXT,
        quantity INTEGER,
        unit_price REAL,
        discount_pct REAL,
        discount_value REAL,
        total REAL,
        payment_type TEXT,
        seller_name TEXT
    )
""")

df.to_sql("sales", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Banco loja_vendas.db criado com sucesso!")



