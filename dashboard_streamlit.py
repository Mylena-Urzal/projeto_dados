#grafico teste 3


import streamlit as st
import pandas as pd
import sqlite3

# 1. CARREGAMENTO E PREPARAÇÃO 
conn = sqlite3.connect("loja_vendas.db")
df = pd.read_sql_query("SELECT * FROM sales", conn, parse_dates=["date"])
conn.close()

# Configurações iniciais
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title("📊 Dashboard de Vendas — Loja de Informática")

# Correção
if 'seller_name' in df.columns:
    df.rename(columns={'seller_name': 'vendedor'}, inplace=True)

# Criação das colunas de tempo
df['date'] = pd.to_datetime(df['date'])
df['Ano'] = df['date'].dt.year
df['Mês'] = df['date'].dt.month
df['Mês_Nome'] = df['date'].dt.strftime('%b') 

# 2. BARRA LATERAL (FILTROS)
st.sidebar.header("Filtros")

# Filtro 1: Ano
anos_disponiveis = sorted(df['Ano'].unique(), reverse=True)
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis)

# Filtro 2: Mês (Multiselect)
# Meses em ordem correta
meses_em_ordem = df.sort_values('Mês')['Mês_Nome'].unique()

meses_selecionados = st.sidebar.multiselect(
    "Selecione os Meses", 
    options=meses_em_ordem, 
    default=meses_em_ordem
)

# Filtro 3: Vendedores
vendedores_disponiveis = df['vendedor'].unique()
vendedores_selecionados = st.sidebar.multiselect(
    "Selecione Vendedores", 
    vendedores_disponiveis, 
    default=vendedores_disponiveis
)

# 3. APLICAR FILTROS (Lógica Principal)

# DF_FILTRADO: Obedece a TUDO (Ano, Mês e Vendedor) -> Para métricas e gráficos do ano atual
df_filtrado = df[
    (df['Ano'] == ano_selecionado) &
    (df['Mês_Nome'].isin(meses_selecionados)) &
    (df['vendedor'].isin(vendedores_selecionados))
]

# DF_COMPARACAO: Obedece Mês e Vendedor, mas PEGA TODOS OS ANOS -> Para o gráfico de comparação
df_comparacao = df[
    (df['Mês_Nome'].isin(meses_selecionados)) &
    (df['vendedor'].isin(vendedores_selecionados))
]

# DASHBOARD

# Se o filtro zerar os dados, avisa
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com esses filtros.")
else:
    #  Métricas (KPIs) 
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Faturamento Total", f"R$ {df_filtrado.total.sum():,.2f}")
    with col2:
        st.metric("Média Diária", f"R$ {df_filtrado.groupby('date').total.sum().mean():,.2f}")

    st.markdown("---") # Linha divisória

    # Divisão para os gráficos principais
    col1_graficos, col2_graficos = st.columns(2)

    with col1_graficos:
        # --- Gráfico 1: Evolução Diária (Do ano selecionado) ---
        st.subheader(f"Evolução Diária de Vendas - {ano_selecionado}")
        st.line_chart(df_filtrado.groupby("date").total.sum())

    with col2_graficos:
        #  Gráfico 2: Vendas Mensais por Vendedor (Novo Gráfico) 
        st.subheader(f"📈 Vendas Mensais por Vendedor - {ano_selecionado}")
        
        # Agrupamento: Soma o total de vendas por Mês e Vendedor
        df_mensal_vendedor = df_filtrado.groupby(['Mês', 'Mês_Nome', 'vendedor'])['total'].sum().reset_index()
        
        # Pivot; Coloca cada vendedor em uma coluna
        df_pivot_vendedor = df_mensal_vendedor.pivot_table(
            index='Mês_Nome',
            columns='vendedor',
            values='total'
        )
        
        # Ordenação correta dos meses
        meses_ordem = df.sort_values('Mês')['Mês_Nome'].unique()
        df_pivot_vendedor = df_pivot_vendedor.reindex(meses_ordem, fill_value=0)

        if not df_pivot_vendedor.empty:
            st.bar_chart(df_pivot_vendedor)
            st.caption("Barra de vendas mensais para cada vendedor no ano e meses selecionados.")
        else:
            st.info("Nenhum dado mensal para os vendedores selecionados.")

    # Gráfico 3: Comparação Ano a Ano (Faturamento Geral)
    st.markdown("---")
    st.header("📈 Comparativo: Ano a Ano")
    st.caption("Este gráfico mostra o faturamento mensal total (de todos os vendedores selecionados) em DIFERENTES ANOS.")

    #  comparação
    df_mensal_yoy = df_comparacao.groupby(['Ano', 'Mês', 'Mês_Nome'])['total'].sum().reset_index()
    
 # Pivot (Linhas = Meses, Colunas = Anos)
    df_pivot_yoy = df_mensal_yoy.pivot_table(
        index='Mês_Nome',
        columns='Ano',
        values='total'
    )
    
    # Ordenar
    meses_ordem_yoy = df.sort_values('Mês')['Mês_Nome'].unique()
    
    if not df_pivot_yoy.empty:
        df_pivot_yoy = df_pivot_yoy.reindex(meses_ordem_yoy)
        st.line_chart(df_pivot_yoy)
    else:
        st.info("Dados insuficientes para comparação anual.")

    #  Tabela
    st.markdown("---")
    with st.expander("Ver Tabela Detalhada"):
        st.dataframe(df_filtrado)