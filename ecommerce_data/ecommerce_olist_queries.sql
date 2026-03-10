-- ============================================
-- BRASIL E-COMMERCE - SQL QUERIES
-- Dataset: Olist Store (96K customers)
-- ============================================

-- TABLA 1: Concentración Geográfica
DROP TABLE IF EXISTS df_brasil_geografia;

CREATE TABLE df_brasil_geografia AS
SELECT 
    customer_state as estado,
    COUNT(customer_id) as total_clientes,
    COUNT(DISTINCT customer_city) as ciudades_cubiertas
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY total_clientes DESC;

-- TABLA 2: Retención de Clientes
DROP TABLE IF EXISTS df_brasil_retencion;

CREATE TABLE df_brasil_retencion AS
SELECT 
    conteo_compras as compras_realizadas,
    COUNT(customer_unique_id) as total_usuarios
FROM (
    SELECT customer_unique_id, COUNT(customer_id) as conteo_compras
    FROM olist_customers_dataset
    GROUP BY customer_unique_id
)
GROUP BY conteo_compras
ORDER BY compras_realizadas ASC;

-- TABLA 3: Oportunidades de Expansión
DROP TABLE IF EXISTS df_brasil_expansion;

CREATE TABLE df_brasil_expansion AS
SELECT 
    customer_state,
    COUNT(customer_id) as clientes,
    CASE 
        WHEN customer_state IN ('SP', 'RJ', 'MG') THEN 'Región Saturada (Sudeste)'
        WHEN customer_state IN ('BA', 'PE', 'CE') THEN 'Región de Expansión (Noreste)'
        ELSE 'Otros Mercados'
    END as categoria_estrategica
FROM olist_customers_dataset
GROUP BY customer_state;

-- TABLA 4: Top 10 Ciudades
DROP TABLE IF EXISTS df_brasil_top_ciudades;

CREATE TABLE df_brasil_top_ciudades AS
SELECT 
    customer_city,
    customer_state,
    COUNT(customer_id) as volumen_clientes
FROM olist_customers_dataset
GROUP BY customer_city, customer_state
ORDER BY volumen_clientes DESC
LIMIT 10;

-- TABLA 5: Densidad por Código Postal
DROP TABLE IF EXISTS df_brasil_logistica;

CREATE TABLE df_brasil_logistica AS
SELECT 
    customer_zip_code_prefix as zip_prefix,
    customer_city,
    COUNT(customer_id) as densidad
FROM olist_customers_dataset
GROUP BY customer_zip_code_prefix
HAVING densidad > 50
ORDER BY densidad DESC;

-- ============================================
-- QUERIES DE ANÁLISIS
-- ============================================

-- Top estados por clientes
SELECT 
    customer_state,
    COUNT(*) as num_clientes,
    COUNT(DISTINCT customer_city) as num_ciudades
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY num_clientes DESC
LIMIT 10;

-- Análisis de regiones
WITH regiones AS (
    SELECT 
        customer_state,
        COUNT(DISTINCT customer_unique_id) as clientes_unicos,
        CASE 
            WHEN customer_state IN ('SP', 'RJ', 'MG', 'ES') THEN 'Sudeste'
            WHEN customer_state IN ('BA', 'SE', 'AL', 'PE', 'PB', 'RN', 'CE', 'PI', 'MA') THEN 'Noreste'
            WHEN customer_state IN ('RS', 'SC', 'PR') THEN 'Sur'
            WHEN customer_state IN ('MT', 'MS', 'GO', 'DF') THEN 'Centro-Oeste'
            WHEN customer_state IN ('AM', 'RR', 'AP', 'PA', 'TO', 'RO', 'AC') THEN 'Norte'
        END as region
    FROM olist_customers_dataset
    GROUP BY customer_state
)
SELECT 
    region,
    SUM(clientes_unicos) as total_clientes,
    ROUND(SUM(clientes_unicos) * 100.0 / (SELECT SUM(clientes_unicos) FROM regiones), 2) as porcentaje
FROM regiones
GROUP BY region
ORDER BY total_clientes DESC;

-- Compras promedio por estado
SELECT 
    customer_state,
    COUNT(DISTINCT customer_unique_id) as clientes_unicos,
    COUNT(*) as total_registros,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT customer_unique_id), 2) as compras_promedio
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY clientes_unicos DESC
LIMIT 10;