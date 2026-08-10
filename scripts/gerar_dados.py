"""
Geração de dataset fictício de operações logísticas.
Estrutura inspirada em um processo real de controle de envios de uma
assistência técnica autorizada, mas com empresas, valores e rastreios
100% inventados para fins de portfólio.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

random.seed(7)
np.random.seed(7)

N = 400

clientes_pf = [
    "Rafaela Monteiro", "Eduardo Vasconcelos", "Priscila Nogueira", "Henrique Salgado",
    "Débora Farias", "Vinícius Cordeiro", "Sabrina Peixoto", "Igor Bezerra",
    "Renata Camargo", "Marcos Aurélio Vieira", "Tatiane Rezende", "Leonardo Guimarães",
    "Cristiane Bittencourt", "Otávio Marinho", "Aline Serpa", "Fabrício Damasceno",
    "Natália Quaresma", "Rodolfo Espíndola", "Simone Aragão", "Gabriel Torquato",
]

clientes_pj = [
    "Constelar Engenharia", "Vórtice Consultoria", "Planalto Distribuidora",
    "Axiom Tecnologia", "Beluga Advocacia", "Cedro Participações",
    "Litoral Alimentos", "Metrópole Logística", "Ipê Educacional",
    "Aliança Cooperativa", "Vantage Digital", "Fortaleza Cimentos",
    "Bem-Estar Hospitalar", "Estrada Real Transportes", "Ventura Seguros",
]

produtos = [
    "iPhone 15", "iPhone 15 Pro", "iPhone 14", "iPhone 13", "MacBook Air",
    "MacBook Pro 14", "MacBook Pro 16", "iPad", "iPad Pro", "iMac",
    "Mac Mini", "Apple Watch", "AirPods Pro", "Trackpad", "Magic Mouse",
    "Cabo USB-C", "Carregador", "Acessórios diversos",
]

transportadoras = ["DHL", "Correios", "FOX", "Retirada no balcão", "Uber", "Correios Seguro"]
transportadora_pesos = [0.30, 0.30, 0.15, 0.12, 0.05, 0.08]

solicitantes = ["Cliente direto", "Filial Regional"]
autorizadores = ["Marcelo", "Vanessa", "Igor", "Patrícia", "Diego", "Sabrina", "Renan"]

status_opcoes = ["Entregue", "Em trânsito", "Pendente de envio", "Devolvido", "Cancelado"]
status_pesos = [0.78, 0.10, 0.06, 0.04, 0.02]

data_inicio = datetime(2025, 8, 1)
data_fim = datetime(2026, 7, 31)
dias_totais = (data_fim - data_inicio).days

rows = []
os_num = 180000

for i in range(N):
    is_pj = random.random() < 0.35
    cliente = random.choice(clientes_pj) if is_pj else random.choice(clientes_pf)
    solicitante = "Filial Regional" if is_pj else "Cliente direto"
    produto = random.choice(produtos)

    base_valor = {
        "iPhone 15 Pro": 8500, "iPhone 15": 6800, "iPhone 14": 5200, "iPhone 13": 4200,
        "MacBook Pro 16": 22000, "MacBook Pro 14": 16000, "MacBook Air": 9500,
        "iPad Pro": 9800, "iPad": 4500, "iMac": 13500, "Mac Mini": 6200,
        "Apple Watch": 3200, "AirPods Pro": 1800, "Trackpad": 750,
        "Magic Mouse": 650, "Cabo USB-C": 120, "Carregador": 250,
        "Acessórios diversos": 400,
    }.get(produto, 1000)
    valor_os = round(max(0.01, np.random.normal(base_valor, base_valor * 0.15)), 2)
    if random.random() < 0.35:
        valor_os = 0.01

    transportadora = random.choices(transportadoras, weights=transportadora_pesos)[0]
    if transportadora == "Retirada no balcão":
        valor_envio = 0.0
        rastreio = "S/N"
    elif transportadora == "Uber":
        valor_envio = round(np.random.uniform(20, 60), 2)
        rastreio = "S/N"
    else:
        peso_fator = {"iPhone 15 Pro":0.6,"iPhone 15":0.6,"iPhone 14":0.6,"iPhone 13":0.6,
                      "MacBook Pro 16":1.8,"MacBook Pro 14":1.6,"MacBook Air":1.3,
                      "iPad Pro":1.0,"iPad":0.9,"iMac":2.5,"Mac Mini":1.4,
                      "Apple Watch":0.4,"AirPods Pro":0.3,"Trackpad":0.3,
                      "Magic Mouse":0.3,"Cabo USB-C":0.2,"Carregador":0.2,
                      "Acessórios diversos":0.3}.get(produto, 0.5)
        base_frete = 45 if transportadora in ("Correios","Correios Seguro") else 130
        valor_envio = round(max(15, np.random.normal(base_frete * (1+peso_fator), 25)), 2)
        prefix = "AD" if transportadora in ("Correios","Correios Seguro") else ""
        rastreio = f"{prefix}{random.randint(100000000,999999999)}BR" if prefix else str(random.randint(1000000000,9999999999))

    dias_offset = random.randint(0, dias_totais)
    data_envio = data_inicio + timedelta(days=dias_offset)

    status = random.choices(status_opcoes, weights=status_pesos)[0]
    prazo_entrega_dias = None
    if status == "Entregue":
        if transportadora == "Uber":
            prazo_entrega_dias = 0
        elif transportadora == "Retirada no balcão":
            prazo_entrega_dias = int(np.random.choice([0,1,2,3],
                                      p=[0.30,0.35,0.20,0.15]))
        else:
            prazo_entrega_dias = int(np.random.choice([1,2,3,4,5,6,7,8,10,14],
                                      p=[0.08,0.14,0.18,0.16,0.12,0.10,0.08,0.06,0.05,0.03]))

    os_num += random.randint(1, 6)

    rows.append({
        "OS": os_num,
        "Data_Solicitacao": data_envio.strftime("%Y-%m-%d"),
        "Cliente": cliente,
        "Tipo_Cliente": "PJ" if is_pj else "PF",
        "Quem_Solicitou": solicitante,
        "Produto": produto,
        "Valor_OS": valor_os,
        "Transportadora": transportadora,
        "Valor_Envio": valor_envio,
        "Rastreio": rastreio,
        "Quem_Autorizou": random.choice(autorizadores),
        "Status": status,
        "Prazo_Entrega_Dias": prazo_entrega_dias,
    })

df = pd.DataFrame(rows).sort_values("Data_Solicitacao").reset_index(drop=True)
df.to_csv(BASE / "data" / "dados_logistica.csv", index=False, encoding="utf-8-sig")
print(df.shape)
print(df.head(10).to_string())
print("\nStatus counts:\n", df["Status"].value_counts())
print("\nTransportadora counts:\n", df["Transportadora"].value_counts())
