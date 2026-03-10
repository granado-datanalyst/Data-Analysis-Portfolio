-- ============================================
-- RETAIL UK - SQL QUERIES
-- Dataset: Online Retail II (1.7M rows)
-- ============================================

-- TABLA 1: Productos Problemáticos
DROP TABLE IF EXISTS df_productos_problematicos;

CREATE TABLE df_productos_problematicos (
    Description TEXT,
    total_perdida REAL,
    num_transacciones INTEGER
);

INSERT INTO df_productos_problematicos VALUES
('?', 1242083.70, 20741),
('damaged', 780988.80, 213968),
('damages', 751853.57, 192385),
('check', 683917.46, 433813),
('missing', 438719.70, 208384),
('smashed', 412184.24, 38238),
('wonky bottom/broken', 327813.65, 25764),
('faulty', 327813.65, 25764),
('broken, uneven bottom', 327813.65, 25764);

-- TABLA 2: Segmentación de Clientes
DROP TABLE IF EXISTS df_segmentacion_clientes;

CREATE TABLE df_segmentacion_clientes AS
SELECT 
    "Customer ID",
    SUM(Quantity * Price) as total_gastado,
    CASE 
        WHEN SUM(Quantity * Price) > 5000 THEN '💎 VIP'
        WHEN SUM(Quantity * Price) > 2000 THEN '🥇 Premium'
        WHEN SUM(Quantity * Price) > 500 THEN '🥈 Regular'
        ELSE '🥉 Ocasional'
    END as categoria_cliente
FROM online_retail_II
WHERE "Customer ID" IS NOT NULL 
  AND "Customer ID" != ''
  AND "Customer ID" != 0
GROUP BY "Customer ID"
HAVING SUM(Quantity * Price) > 0;

-- TABLA 3: Performance por Región
DROP TABLE IF EXISTS df_performance_regiones;

CREATE TABLE df_performance_regiones AS
SELECT 
    Country,
    SUM(Quantity * Price) as ventas_totales,
    CASE 
        WHEN SUM(Quantity * Price) > 50000 THEN '🔥 Excelente'
        WHEN SUM(Quantity * Price) > 10000 THEN '👍 Bueno'
        ELSE '⚠️ Bajo'
    END as performance
FROM online_retail_II
GROUP BY Country
ORDER BY ventas_totales DESC;

-- TABLA 4: Top 10 Productos
DROP TABLE IF EXISTS df_top_productos;

CREATE TABLE df_top_productos AS
SELECT 
    Description,
    SUM(Quantity * Price) as revenue_total,
    SUM(Quantity) as unidades_vendidas
FROM online_retail_II
WHERE Description NOT LIKE '%?%'
GROUP BY Description
ORDER BY revenue_total DESC
LIMIT 10;

-- TABLA 5: Ticket Promedio por País
DROP TABLE IF EXISTS df_ticket_promedio_paises;

CREATE TABLE df_ticket_promedio_paises AS
SELECT 
    Country,
    ROUND(AVG(Quantity * Price), 2) as ticket_promedio,
    COUNT(DISTINCT Invoice) as total_facturas
FROM online_retail_II
GROUP BY Country
HAVING total_facturas > 100
ORDER BY ticket_promedio DESC;

-- ============================================
-- QUERIES DE ANÁLISIS (para referencia)
-- ============================================

-- Top 10 productos por ingresos
SELECT 
    Description,
    ROUND(SUM(Quantity * Price), 2) as ingresos_totales,
    SUM(Quantity) as unidades_vendidas
FROM online_retail_II
GROUP BY Description
ORDER BY ingresos_totales DESC
LIMIT 10;

-- Ventas por región
SELECT 
    Country,
    COUNT(DISTINCT "Customer ID") as num_clientes,
    COUNT(*) as num_ordenes,
    ROUND(SUM(Quantity * Price), 2) as ventas_totales
FROM online_retail_II
GROUP BY Country
ORDER BY ventas_totales DESC;

-- Clientes VIP
SELECT 
    "Customer ID",
    SUM(Quantity * Price) as total_gastado,
    COUNT(*) as num_compras
FROM online_retail_II
WHERE "Customer ID" IS NOT NULL
GROUP BY "Customer ID"
HAVING SUM(Quantity * Price) > 5000
ORDER BY total_gastado DESC;