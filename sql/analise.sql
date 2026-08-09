-- ============================================================
-- Análise de Operações Logísticas — Consultas SQL
-- Banco: SQLite (tabela: envios)
-- Autor: Lucas | Projeto de portfólio
-- ============================================================

-- 1) Volume e valor total de frete por transportadora
SELECT
    Transportadora,
    COUNT(*)                       AS qtd_envios,
    ROUND(SUM(Valor_Envio), 2)     AS custo_total_frete,
    ROUND(AVG(Valor_Envio), 2)     AS custo_medio_frete
FROM envios
GROUP BY Transportadora
ORDER BY custo_total_frete DESC;

-- 2) Taxa de entrega por status
SELECT
    Status,
    COUNT(*) AS qtd,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM envios), 2) AS pct_do_total
FROM envios
GROUP BY Status
ORDER BY qtd DESC;

-- 3) Prazo médio de entrega (dias) por transportadora — apenas pedidos entregues
SELECT
    Transportadora,
    COUNT(*)                            AS qtd_entregas,
    ROUND(AVG(Prazo_Entrega_Dias), 1)   AS prazo_medio_dias,
    MIN(Prazo_Entrega_Dias)             AS prazo_minimo,
    MAX(Prazo_Entrega_Dias)             AS prazo_maximo
FROM envios
WHERE Status = 'Entregue'
GROUP BY Transportadora
ORDER BY prazo_medio_dias ASC;

-- 4) Evolução mensal de envios e custo de frete
SELECT
    strftime('%Y-%m', Data_Solicitacao) AS mes,
    COUNT(*)                            AS qtd_envios,
    ROUND(SUM(Valor_Envio), 2)          AS custo_frete_total,
    ROUND(SUM(Valor_OS), 2)             AS valor_os_total
FROM envios
GROUP BY mes
ORDER BY mes;

-- 5) Top 10 clientes por valor total movimentado (Valor_OS)
SELECT
    Cliente,
    Tipo_Cliente,
    COUNT(*)                    AS qtd_os,
    ROUND(SUM(Valor_OS), 2)     AS valor_total
FROM envios
GROUP BY Cliente, Tipo_Cliente
ORDER BY valor_total DESC
LIMIT 10;

-- 6) Custo de frete como % do valor da OS, por produto (produtos com valor de OS > 0)
SELECT
    Produto,
    COUNT(*)                                          AS qtd,
    ROUND(AVG(Valor_Envio), 2)                         AS frete_medio,
    ROUND(AVG(Valor_OS), 2)                            AS valor_os_medio,
    ROUND(100.0 * AVG(Valor_Envio) / NULLIF(AVG(NULLIF(Valor_OS,0.01)),0), 2) AS pct_frete_sobre_os
FROM envios
GROUP BY Produto
ORDER BY qtd DESC;

-- 7) Pedidos pendentes/em risco (não entregues) por responsável que autorizou
SELECT
    Quem_Autorizou,
    Status,
    COUNT(*) AS qtd
FROM envios
WHERE Status IN ('Pendente de envio', 'Em trânsito', 'Devolvido', 'Cancelado')
GROUP BY Quem_Autorizou, Status
ORDER BY Quem_Autorizou, qtd DESC;

-- 8) Clientes PJ (filiais) vs PF (clientes diretos): comparação de ticket médio
SELECT
    Tipo_Cliente,
    COUNT(*)                    AS qtd_os,
    ROUND(AVG(Valor_OS), 2)     AS ticket_medio,
    ROUND(AVG(Valor_Envio), 2)  AS frete_medio
FROM envios
GROUP BY Tipo_Cliente;
