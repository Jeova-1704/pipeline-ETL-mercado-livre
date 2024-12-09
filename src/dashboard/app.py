import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("../../data/database.db")

df = pd.read_sql_query("SELECT * FROM produtos", conn)

conn.close()

st.title("Dashboard da pesquisa de mercado de tênis do mercado livre")

st.subheader("KPIs principais do mercado de tênis do mercado livre")

col1, col2, col3 = st.columns(3)

total_produtos = df.shape[0]
col1.metric(label="Total de produtos", value=total_produtos)

marcas_unicas = df["marca"].nunique()
col2.metric(label="Marcas únicas", value=marcas_unicas)

preco_medio = df["preco_atual"].mean()
col3.metric(label="Preço médio (R$)", value=f" R${preco_medio:.2f}")

st.subheader("Marcas mais encontradas até a pagina 10")
col1, col2 = st.columns([4, 2])

top_10_marcas = df["marca"].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_marcas)
col2.write(top_10_marcas)

st.subheader("Preço médio por marca")
col1, col2 = st.columns([4, 2])
df_no_zero_price = df[df['preco_atual'] > 0]
preco_medio_por_marca = df_no_zero_price.groupby("marca")["preco_atual"].mean().sort_values(ascending=False)
col1.bar_chart(round(preco_medio_por_marca, 2))
col2.write(round(preco_medio_por_marca, 2))

st.subheader("Sastifação por marca")
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['avaliacao'] > 0]
satisfacao_por_marca = df_non_zero_reviews.groupby("marca")["avaliacao"].mean().sort_values(ascending=False)
col1.bar_chart(round(satisfacao_por_marca, 2))
col2.write(round(satisfacao_por_marca, 2))

