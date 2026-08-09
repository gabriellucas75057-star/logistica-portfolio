"""
Análise de Operações Logísticas — Python (pandas + matplotlib)

Este script:
1. Carrega o dataset
2. Calcula KPIs operacionais
3. Gera 4 gráficos profissionais para o relatório/portfólio
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE / "data" / "dados_logistica.csv", parse_dates=["Data_Solicitacao"])

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#444444"
plt.rcParams["axes.labelcolor"] = "#333333"
plt.rcParams["text.color"] = "#333333"
plt.rcParams["xtick.color"] = "#333333"
plt.rcParams["ytick.color"] = "#333333"
COLOR_PRIMARY = "#1f6feb"
COLOR_ACCENT = "#2ea043"
COLOR_WARN = "#d29922"
COLOR_MUTED = "#8b949e"

# ---------------------------------------------------------------
# KPIs gerais
# ---------------------------------------------------------------
total_envios = len(df)
total_frete = df["Valor_Envio"].sum()
frete_medio = df["Valor_Envio"].mean()
taxa_entrega = (df["Status"] == "Entregue").mean() * 100
prazo_medio = df.loc[df["Status"] == "Entregue", "Prazo_Entrega_Dias"].mean()

print("=" * 60)
print("KPIs GERAIS")
print("=" * 60)
print(f"Total de envios:            {total_envios}")
print(f"Custo total de frete:       R$ {total_frete:,.2f}")
print(f"Custo médio por envio:      R$ {frete_medio:,.2f}")
print(f"Taxa de entrega concluída:  {taxa_entrega:.1f}%")
print(f"Prazo médio de entrega:     {prazo_medio:.1f} dias")

# ---------------------------------------------------------------
# Gráfico 1 — Custo de frete por transportadora
# ---------------------------------------------------------------
g1 = df.groupby("Transportadora")["Valor_Envio"].sum().sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(g1.index, g1.values, color=COLOR_PRIMARY)
ax.set_title("Custo total de frete por transportadora", fontsize=13, fontweight="bold", loc="left")
ax.set_xlabel("Valor (R$)")
for bar in bars:
    w = bar.get_width()
    ax.text(w + max(g1.values) * 0.01, bar.get_y() + bar.get_height()/2,
            f"R$ {w:,.0f}", va="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(BASE / "charts" / "01_custo_por_transportadora.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# Gráfico 2 — Evolução mensal do volume de envios
# ---------------------------------------------------------------
df["mes"] = df["Data_Solicitacao"].dt.to_period("M").astype(str)
g2 = df.groupby("mes").size()
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(g2.index, g2.values, marker="o", color=COLOR_PRIMARY, linewidth=2)
ax.fill_between(g2.index, g2.values, color=COLOR_PRIMARY, alpha=0.08)
ax.set_title("Evolução mensal do volume de envios", fontsize=13, fontweight="bold", loc="left")
ax.set_ylabel("Qtd. de envios")
plt.xticks(rotation=45, ha="right")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(BASE / "charts" / "02_evolucao_mensal.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# Gráfico 3 — Distribuição de status dos envios
# ---------------------------------------------------------------
g3 = df["Status"].value_counts()
colors = [COLOR_ACCENT, COLOR_PRIMARY, COLOR_WARN, "#f85149", COLOR_MUTED]
fig, ax = plt.subplots(figsize=(6.5, 5))
wedges, texts, autotexts = ax.pie(
    g3.values, labels=g3.index, autopct="%1.1f%%", startangle=90,
    colors=colors[:len(g3)], pctdistance=0.8,
    wedgeprops={"width": 0.42, "edgecolor": "white", "linewidth": 2}
)
for t in autotexts:
    t.set_color("white")
    t.set_fontsize(9)
    t.set_fontweight("bold")
ax.set_title("Distribuição dos envios por status", fontsize=13, fontweight="bold", loc="left")
plt.tight_layout()
plt.savefig(BASE / "charts" / "03_status_envios.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# Gráfico 4 — Prazo médio de entrega por transportadora
# ---------------------------------------------------------------
g4 = (
    df[df["Status"] == "Entregue"]
    .groupby("Transportadora")["Prazo_Entrega_Dias"]
    .mean()
    .sort_values()
)
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(g4.index, g4.values, color=COLOR_ACCENT)
ax.set_title("Prazo médio de entrega por transportadora (dias)", fontsize=13, fontweight="bold", loc="left")
ax.set_ylabel("Dias")
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.1, f"{h:.1f}", ha="center", fontsize=9)
plt.xticks(rotation=20, ha="right")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(BASE / "charts" / "04_prazo_por_transportadora.png", dpi=150)
plt.close()

print("\nGráficos salvos em /charts")
