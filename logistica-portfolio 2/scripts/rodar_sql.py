"""
Carrega o CSV em um banco SQLite e roda as consultas de sql/analise.sql,
imprimindo os resultados formatados. Isso simula um pipeline real de
análise: dados -> banco -> SQL -> insights.
"""
import sqlite3
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
csv_path = BASE / "data" / "dados_logistica.csv"
sql_path = BASE / "sql" / "analise.sql"
db_path = BASE / "data" / "logistica.db"

df = pd.read_csv(csv_path)

conn = sqlite3.connect(db_path)
df.to_sql("envios", conn, if_exists="replace", index=False)

sql_script = sql_path.read_text(encoding="utf-8")

def clean_statement(chunk: str) -> str:
    lines = [ln for ln in chunk.splitlines() if not ln.strip().startswith("--")]
    return "\n".join(lines).strip()

# separa em statements individuais (split simples por ";"), removendo comentários linha a linha
raw_chunks = sql_script.split(";")
statements = [clean_statement(c) for c in raw_chunks]
statements = [s for s in statements if s]

titles = [
    "1) Volume e custo de frete por transportadora",
    "2) Taxa de status dos envios",
    "3) Prazo médio de entrega por transportadora",
    "4) Evolução mensal de envios e custo",
    "5) Top 10 clientes por valor movimentado",
    "6) Custo de frete (%) sobre valor da OS, por produto",
    "7) Pedidos em risco por responsável",
    "8) PJ vs PF: ticket médio e frete médio",
]

for title, stmt in zip(titles, statements):
    print("=" * 70)
    print(title)
    print("=" * 70)
    try:
        result = pd.read_sql_query(stmt, conn)
        print(result.to_string(index=False))
    except Exception as e:
        print("Erro:", e)
    print()

conn.close()
print(f"\nBanco salvo em: {db_path}")
