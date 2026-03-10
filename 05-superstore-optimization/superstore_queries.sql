-- ============================================
-- SUPERSTORE - SQL QUERIES
-- Dataset: Global SuperStore (51K orders)
-- ============================================

-- TABLA 1: Análisis de Descuentos
DROP TABLE IF EXISTS df_superstore_descuentos;

CREATE TABLE df_superstore_descuentos AS
SELECT 
    discount as nivel_descuento,
    ROUND(AVG(profit), 2) as ganancia_promedio,
    ROUND(SUM(CAST(sales AS REAL)), 2) as volumen_ventas,
    COUNT(*) as cantidad_operaciones
FROM SuperStoreOrders
GROUP BY discount
ORDER BY discount ASC;

-- TABLA 2: Productos Críticos (con pérdidas)
DROP TABLE IF EXISTS df_superstore_productos_criticos;

CREATE TABLE df_superstore_productos_criticos AS
SELECT 
    product_name,
    category,
    ROUND(SUM(CAST(sales AS REAL)), 2) as ventas_totales,
    ROUND(SUM(profit), 2) as perdida_total
FROM SuperStoreOrders
GROUP BY product_name, category
HAVING SUM(profit) < 0
ORDER BY perdida_total ASC
LIMIT 10;

-- TABLA 3: Rentabilidad por Categoría
DROP TABLE IF EXISTS df_superstore_categorias;

CREATE TABLE df_superstore_categorias AS
SELECT 
    category,
    sub_category,
    ROUND(SUM(CAST(sales AS REAL)), 2) as ventas_totales,
    ROUND(SUM(profit), 2) as ganancia_total,
    ROUND((SUM(profit) / SUM(CAST(sales AS REAL))) * 100, 2) as margen_porcentaje
FROM SuperStoreOrders
GROUP BY category, sub_category
ORDER BY ganancia_total DESC;

-- TABLA 4: Análisis Logístico
DROP TABLE IF EXISTS df_superstore_logistica;

CREATE TABLE df_superstore_logistica AS
SELECT 
    ship_mode,
    ROUND(AVG(shipping_cost), 2) as costo_envio_promedio,
    ROUND(SUM(profit), 2) as ganancia_por_metodo,
    COUNT(*) as num_operaciones
FROM SuperStoreOrders
GROUP BY ship_mode
ORDER BY costo_envio_promedio DESC;

-- TABLA 5: Performance Regional
DROP TABLE IF EXISTS df_superstore_regiones;

CREATE TABLE df_superstore_regiones AS
SELECT 
    market,
    region,
    ROUND(SUM(CAST(sales AS REAL)), 2) as ventas,
    ROUND(SUM(profit), 2) as ganancia,
    COUNT(DISTINCT customer_name) as clientes_unicos
FROM SuperStoreOrders
GROUP BY market, region
ORDER BY ganancia DESC;

-- ============================================
-- QUERIES DE ANÁLISIS
-- ============================================

-- Top 10 productos rentables
SELECT 
    product_name,
    category,
    sub_category,
    COUNT(*) as num_ventas,
    ROUND(SUM(CAST(sales AS REAL)), 2) as ventas_totales,
    ROUND(SUM(profit), 2) as profit_total
FROM SuperStoreOrders
GROUP BY product_name, category, sub_category
ORDER BY profit_total DESC
LIMIT 10;

-- Impacto de descuentos
SELECT 
    CASE 
        WHEN discount = 0 THEN 'Sin descuento'
        WHEN discount <= 0.1 THEN '1-10%'
        WHEN discount <= 0.2 THEN '11-20%'
        WHEN discount <= 0.3 THEN '21-30%'
        ELSE 'Más de 30%'
    END as rango_descuento,
    COUNT(*) as num_ventas,
    ROUND(AVG(CAST(sales AS REAL)), 2) as venta_promedio,
    ROUND(AVG(profit), 2) as profit_promedio,
    ROUND(AVG(profit) * 100.0 / AVG(CAST(sales AS REAL)), 2) as margen_pct
FROM SuperStoreOrders
GROUP BY rango_descuento
ORDER BY rango_descuento;

-- Ranking por categoría (Window Functions)
WITH productos_rankeados AS (
    SELECT 
        category,
        product_name,
        ROUND(SUM(profit), 2) as profit_total,
        ROW_NUMBER() OVER (
            PARTITION BY category 
            ORDER BY SUM(profit) DESC
        ) as ranking
    FROM SuperStoreOrders
    GROUP BY category, product_name
)
SELECT 
    category,
    product_name,
    profit_total,
    ranking
FROM productos_rankeados
WHERE ranking <= 3
ORDER BY category, ranking;

-- Ventas por región
SELECT 
    region,
    COUNT(DISTINCT customer_name) as num_clientes,
    COUNT(*) as num_ordenes,
    ROUND(SUM(CAST(sales AS REAL)), 2) as ventas_totales,
    ROUND(SUM(profit), 2) as profit_total,
    ROUND(SUM(profit) * 100.0 / SUM(CAST(sales AS REAL)), 2) as margen_profit_pct
FROM SuperStoreOrders
GROUP BY region
ORDER BY ventas_totales DESC;