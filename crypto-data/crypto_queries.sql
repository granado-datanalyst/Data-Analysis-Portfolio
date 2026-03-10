-- ============================================
-- CRYPTO FRAUD DETECTION - SQL QUERIES
-- Dataset: Ethereum Fraud (9,841 accounts)
-- ============================================

-- TABLA 1: Perfil de Riesgo
DROP TABLE IF EXISTS df_crypto_perfil_riesgo;

CREATE TABLE df_crypto_perfil_riesgo AS
SELECT 
    FLAG as es_fraude, 
    COUNT(*) as total_cuentas,
    AVG("Avg min between sent tnx") as promedio_tiempo_envio,
    AVG("Avg min between received tnx") as promedio_tiempo_recibo,
    AVG(" Total ERC20 tnxs") as promedio_transacciones_erc20
FROM transactions
GROUP BY FLAG;

-- TABLA 2: Detección de Bots por Velocidad
DROP TABLE IF EXISTS df_crypto_velocidad_bots;

CREATE TABLE df_crypto_velocidad_bots AS
SELECT 
    CASE 
        WHEN "Avg min between sent tnx" < 1 THEN '⚡ Bot / Script ( < 1 min)'
        WHEN "Avg min between sent tnx" BETWEEN 1 AND 60 THEN '🏃 Humano Activo (1h)'
        ELSE '🐢 Inactivo / Long-term'
    END as categoria_velocidad,
    FLAG as es_fraude,
    COUNT(*) as cantidad_direcciones
FROM transactions
GROUP BY categoria_velocidad, FLAG;

-- TABLA 3: Análisis de Volumen
DROP TABLE IF EXISTS df_crypto_volumen_ether;

CREATE TABLE df_crypto_volumen_ether AS
SELECT 
    FLAG as es_fraude,
    MIN("total Ether sent") as min_enviado,
    MAX("total Ether sent") as max_enviado,
    AVG("total Ether sent") as promedio_enviado,
    SUM("total Ether sent") as volumen_total_movido
FROM transactions
GROUP BY FLAG;

-- TABLA 4: Tokens Sospechosos
DROP TABLE IF EXISTS df_crypto_tokens_sospechosos;

CREATE TABLE df_crypto_tokens_sospechosos AS
SELECT 
    " ERC20 most sent token type" as token_name,
    COUNT(*) as menciones,
    SUM(FLAG) as casos_fraude_confirmados
FROM transactions
WHERE " ERC20 most sent token type" IS NOT NULL 
  AND " ERC20 most sent token type" != '0'
  AND " ERC20 most sent token type" != ''
  AND TRIM(" ERC20 most sent token type") != ''
  AND LENGTH(" ERC20 most sent token type") > 1
GROUP BY " ERC20 most sent token type"
ORDER BY casos_fraude_confirmados DESC
LIMIT 15;

-- TABLA 5: Vulnerabilidad (Balance Cero)
DROP TABLE IF EXISTS df_crypto_vulnerabilidad;

CREATE TABLE df_crypto_vulnerabilidad AS
SELECT 
    FLAG as es_fraude,
    COUNT(*) as cuentas_balance_cero
FROM transactions
WHERE "total ether balance" = 0
GROUP BY FLAG;

-- ============================================
-- QUERIES DE ANÁLISIS
-- ============================================

-- Balance fraude vs válido
SELECT 
    CASE WHEN FLAG = 0 THEN 'Valid' ELSE 'Fraud' END as tipo,
    COUNT(*) as num_transacciones,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as porcentaje
FROM transactions
GROUP BY FLAG;

-- Análisis de valores
SELECT 
    CASE WHEN FLAG = 0 THEN 'Valid' ELSE 'Fraud' END as tipo,
    ROUND(AVG("total Ether sent"), 2) as avg_ether_enviado,
    ROUND(AVG("total ether received"), 2) as avg_ether_recibido,
    ROUND(AVG("total ether balance"), 2) as avg_balance
FROM transactions
GROUP BY FLAG;

-- Top 10 cuentas fraudulentas
SELECT 
    Address,
    "total transactions (including tnx to create contract" as total_trans,
    "Sent tnx" as enviadas,
    "Received Tnx" as recibidas,
    ROUND("total Ether sent", 2) as ether_enviado,
    " ERC20 most sent token type" as token_principal
FROM transactions
WHERE FLAG = 1
ORDER BY "total transactions (including tnx to create contract" DESC
LIMIT 10;

-- Segmentación por actividad
WITH actividad_categorizada AS (
    SELECT 
        Address,
        FLAG,
        "total transactions (including tnx to create contract" as total_trans,
        CASE 
            WHEN "total transactions (including tnx to create contract" > 1000 THEN 'Muy Alta'
            WHEN "total transactions (including tnx to create contract" > 100 THEN 'Alta'
            WHEN "total transactions (including tnx to create contract" > 10 THEN 'Media'
            ELSE 'Baja'
        END as nivel_actividad
    FROM transactions
)
SELECT 
    nivel_actividad,
    CASE WHEN FLAG = 0 THEN 'Valid' ELSE 'Fraud' END as tipo,
    COUNT(*) as num_cuentas,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY nivel_actividad), 2) as porcentaje
FROM actividad_categorizada
GROUP BY nivel_actividad, FLAG
ORDER BY 
    CASE nivel_actividad 
        WHEN 'Muy Alta' THEN 1 
        WHEN 'Alta' THEN 2 
        WHEN 'Media' THEN 3 
        ELSE 4 
    END,
    FLAG;

-- Análisis temporal
SELECT 
    CASE WHEN FLAG = 0 THEN 'Valid' ELSE 'Fraud' END as tipo,
    CASE 
        WHEN "Avg min between sent tnx" = 0 THEN 'Instantáneo'
        WHEN "Avg min between sent tnx" < 1 THEN 'Muy Rápido (<1 min)'
        WHEN "Avg min between sent tnx" < 60 THEN 'Rápido (<1 hora)'
        WHEN "Avg min between sent tnx" < 1440 THEN 'Normal (<1 día)'
        ELSE 'Lento (>1 día)'
    END as velocidad,
    COUNT(*) as num_cuentas
FROM transactions
GROUP BY FLAG, velocidad
ORDER BY FLAG;

-- Modelo de riesgo
WITH risk_scores AS (
    SELECT 
        Address,
        FLAG,
        (CASE WHEN "Avg min between sent tnx" < 1 THEN 3 ELSE 0 END +
         CASE WHEN "Received Tnx" = 0 AND "Sent tnx" > 10 THEN 3 ELSE 0 END +
         CASE WHEN "total transactions (including tnx to create contract" > 1000 THEN 2 ELSE 0 END +
         CASE WHEN "Received Tnx" > 0 AND CAST("Sent tnx" AS REAL)/"Received Tnx" > 10 THEN 2 ELSE 0 END +
         CASE WHEN "Number of Created Contracts" > 5 THEN 2 ELSE 0 END
        ) as risk_score
    FROM transactions
)
SELECT 
    CASE 
        WHEN risk_score >= 8 THEN 'Alto Riesgo'
        WHEN risk_score >= 5 THEN 'Medio Riesgo'
        WHEN risk_score >= 2 THEN 'Bajo Riesgo'
        ELSE 'Sin Riesgo'
    END as categoria,
    CASE WHEN FLAG = 0 THEN 'Valid' ELSE 'Fraud' END as tipo,
    COUNT(*) as num_cuentas
FROM risk_scores
GROUP BY categoria, FLAG
ORDER BY 
    CASE categoria
        WHEN 'Alto Riesgo' THEN 1
        WHEN 'Medio Riesgo' THEN 2
        WHEN 'Bajo Riesgo' THEN 3
        ELSE 4
    END,
    FLAG;