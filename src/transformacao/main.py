import pandas as pd
import sqlite3
from datetime import datetime
"""
marca,
nome,
preco_antigo,
centavos_antigo,
preco_atual,
centavos_atual,
avaliacao,
quantidade_avaliacoes
"""
file_path = "../../data/data.csv"


df = pd.read_csv(file_path)

df['source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

df['data_coleta'] = datetime.now()

df['preco_antigo'] = df['preco_antigo'].fillna(0).astype(float)
df['preco_atual'] = df['preco_atual'].fillna(0).astype(float)
df['centavos_antigo'] = df['centavos_antigo'].fillna(0).astype(float)
df['centavos_atual'] = df['centavos_atual'].fillna(0).astype(float)


df['quantidade_avaliacoes'] = df['quantidade_avaliacoes'].str.replace('[\(\)]', '', regex=True)
df['quantidade_avaliacoes'] = df['quantidade_avaliacoes'].fillna(0).astype(int)


df['preco_antigo'] = df['preco_antigo'] + (df['centavos_antigo'] / 100)
df['preco_atual'] = df['preco_atual'] + (df['centavos_atual'] / 100)

df = df.drop(columns=['centavos_antigo', 'centavos_atual'])

conn = sqlite3.connect("../../data/database.db")

df.to_sql('produtos', conn, if_exists='replace', index=False)

conn.close()

print('Dados transformados e salvos com sucesso!')