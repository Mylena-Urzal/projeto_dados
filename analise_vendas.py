# PROJETO ANALISE DE DADOS

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("loja_vendas.db")

sales = pd.read_sql_query("SELECT * FROM sales", conn, parse_dates=["date"])
sellers = pd.read_sql_query("SELECT * FROM sellers", conn)
conn.close()

sales["year"] = sales["date"].dt.year
sales["year_month"] = sales["date"].dt.to_period("M")

# MEDIA ANUAL POR VENDEDOR

dias_ano = {2024: 366, 2025: 365}

annual = sales.groupby(["seller_name", "year"]).total.sum().reset_index()
annual["dias"] = annual["year"].apply(lambda x: dias_ano[x])
annual["media_diaria"] = annual["total"] / annual["dias"]

print("\n MÉDIA DIÁRIA ANUAL POR VENDEDOR:")
print(annual)

# COMPARAÇÃO ANUAL

ranking = sales.groupby("seller_name").total.sum().reset_index()
ranking = ranking.sort_values("total", ascending=False)

print("\n RANKING DE VENDEDORES (2 anos):")
print(ranking)

# COMISSAO 

monthly = sales.groupby(["seller_name", "year_month"]).total.sum().reset_index()
monthly["commission"] = monthly["total"] * 0.03

monthly = monthly.merge(sellers, on="seller_name")
monthly["recebido"] = monthly["commission"] + monthly["base_salary"]

print("\n SALÁRIO + COMISSÃO (mensal):")
print(monthly.head())

# GRÁFICO 

#TOTAL POR VENDEDOR
graf1 = ranking.plot(x="seller_name", y="total", kind="bar", title="Total de Vendas por Vendedor")
plt.tight_layout()
plt.savefig("total_by_seller.png")
plt.close()

# MÉDIA DIÁRIA POR VENDEDOR

graf2 = annual.groupby("seller_name").media_diaria.mean().plot(kind="bar", title="Média Diária por Vendedor")
plt.tight_layout()
plt.savefig("avg_daily_by_seller.png")
plt.close()

# 30 DIAS

daily = sales.groupby("date").total.sum().reset_index()
daily["rolling"] = daily["total"].rolling(30).mean()

graf3 = daily.plot(x="date", y=["total", "rolling"], title="Vendas Diárias vs Média Móvel 30 dias")
plt.axhline(800, color="red", linestyle="--", label="Meta diária")
plt.tight_layout()
plt.savefig("daily_rolling_vs_target.png")
plt.close()

print("\nGráficos salvos!")



