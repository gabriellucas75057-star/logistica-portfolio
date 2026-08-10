#  Análise de Operações Logísticas

Projeto de análise de dados aplicado a um processo real de controle de envios, com **Python, SQL e visualização de dados**, construído a partir da minha experiência profissional em operações logísticas.

> ⚠️ **Nota sobre os dados**: o dataset usado neste projeto é **sintético (fictício)**, gerado para reproduzir a estrutura e os padrões de um processo real de controle de envios de uma assistência técnica autorizada, sem expor nenhuma informação confidencial de empresas ou clientes reais.

---

##  Contexto

Trabalho há quase 8 meses na área operacional/logística de uma autorizada Apple em Curitiba, onde lido diariamente com controle de ordens de serviço, acompanhamento de transportadoras (DHL, Correios, FOX, retirada local), planilhas de gestão e organização de informações operacionais.

Esse projeto nasceu de perguntas que eu via surgir na minha própria rotina de trabalho, e que decidi responder com dados de verdade:

- Qual transportadora tem o **melhor custo-benefício**?
- Qual o **prazo médio de entrega** por transportadora?
- Como o **volume de envios** evolui mês a mês?
- Qual a **taxa de entregas concluídas** vs. pendências/devoluções?
- Onde estão os **maiores custos de frete** em relação ao valor transportado?

##  Stack utilizada

| Ferramenta | Uso no projeto |
|---|---|
| **Python** (pandas, matplotlib) | Limpeza, cálculo de KPIs e geração de gráficos |
| **SQL** (SQLite) | Consultas analíticas (agregações, agrupamentos, métricas) |
| **Git/GitHub** | Versionamento e portfólio público |
| **CSV / dados tabulares** | Base de dados do projeto |

## 📁 Estrutura do repositório

logistica-portfolio/
├── data/
│ └── dados_logistica.csv # dataset (400 registros fictícios)
├── scripts/
│ ├── gerar_dados.py # geração do dataset sintético
│ ├── analise.py # análise + geração dos gráficos
│ └── rodar_sql.py # executa as queries SQL sobre os dados
├── sql/
│ └── analise.sql # 8 consultas analíticas comentadas
├── charts/ # gráficos gerados (.png)
└── README.md
##  Principais insights

- **DHL e FOX concentram ~78% do custo total de frete**, mesmo não sendo as transportadoras com maior volume — indicando oportunidade de renegociação ou redistribuição de envios.
- **Uber tem o menor prazo médio de entrega (3,7 dias)** entre as opções analisadas, seguido de retirada no balcão.
- **~79% dos envios são concluídos com sucesso**; o restante se divide entre pendentes, em trânsito, devolvidos e cancelados — um indicador direto de saúde operacional.
- Itens de baixo valor (cabos, carregadores) têm o **frete representando até 82% do valor do produto**, um ponto de atenção para revisão de política de envio desses itens.
- Clientes **PF têm ticket médio ligeiramente maior que PJ** neste recorte, o que reforça a importância de segmentar a análise por tipo de cliente em vez de assumir padrões fixos.

##  Como rodar o projeto

```bash
git clone https://github.com/gabriellucas75057-star/logistica-portfolio.git
cd logistica-portfolio
pip install pandas matplotlib

python scripts/gerar_dados.py   # gera o dataset
python scripts/analise.py       # gera os gráficos em /charts
python scripts/rodar_sql.py     # roda as 8 consultas SQL
```

## 👤 Sobre mim

Sou profissional de operações e logística, hoje atuando em uma autorizada Apple em Curitiba, e estou em transição para análise de dados — cursando Análise e Desenvolvimento de Sistemas (ADS) na UNINTER. Este é o primeiro de uma série de projetos que venho construindo para transformar experiência operacional real em análise de dados aplicada.

 [linkedin.com/in/lucasgabriel7](https://www.linkedin.com/in/lucasgabriel7/)
