# 🛒 SuperStore - Profit Optimization

![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![BI](https://img.shields.io/badge/Business-Intelligence-orange?style=flat)

**Pricing strategy analysis uncovering $210K in annual improvement opportunities**

[📊 Live Demo](#) | [💻 Dashboard Code](superstore_dashboard_ENES.py) | [🗃️ SQL Queries](superstore_queries.sql)

---

## 🇬🇧 English

### 📋 Executive Summary

**Business Problem:** Global retail company with uncontrolled discount policy destroying profit margins across 51K orders.

**Solution:** Comprehensive profitability analysis using SQL (CTEs, Aggregations, Window Functions) to identify discount impact and loss-making products.

**Results:**
- 💰 **$210K/year** savings identified
- 🚨 **Discounts >20%** generate -68% margin
- 📦 **$40K losses** from 10 specific products
- 🎯 **58% precision** in identifying at-risk items

---

### 🔍 Key Findings

#### 1. Destructive Discount Policy

**The Discount Margin Cliff:**

| Discount Range | Avg Margin | Status |
|---------------|------------|---------|
| 0% (No discount) | **+41%** | ✅ Healthy |
| 1-10% | **+30%** | ✅ Acceptable |
| 11-20% | **+16%** | ⚠️ Borderline |
| 21-30% | **-8.7%** | 🚨 LOSS |
| >30% | **-68.8%** | 💀 CRITICAL |

**Root Cause:** No approval process for discounts >15%. Sales team had unlimited authority.

**Impact:**
- 10,361 orders with >30% discount
- Average loss per order: -$76.59
- **Annual impact: ~$80K in losses**

**Recommended Action:**
```
IMMEDIATE:
- Maximum discount: 15%
- Manager approval required for >10%
- Remove unlimited discount authority

Expected savings: $80K/year
```

---

#### 2. Loss-Making Products

**Top 10 Products Hemorrhaging Money:**

| Product | Category | Loss |
|---------|----------|------|
| Cubify 3D Printer Double Head | Technology | -$8,880 |
| Lexmark Printer | Technology | -$4,590 |
| Motorola Phone Cordless | Technology | -$4,447 |
| Bevis Round Table | Furniture | -$3,650 |
| Rogers Lockers Blue | Office Supplies | -$2,893 |
| ... | ... | ... |
| **TOTAL** | **All** | **-$40,072** |

**Why Losses Occur:**
```
Example: Rogers Lockers Blue
- Cost: $100 (product) + $15 (shipping + processing)
- Price: $150
- 30% discount applied: $105 final price
- Result: -$10 loss per unit
- Sold 42 units = -$2,893 total loss
```

**Recommended Actions:**
```
Priority 1: Discontinue top 3 loss-makers
Priority 2: Increase pricing on remaining 7
Priority 3: Audit all products with <5% margin

Expected recovery: $40K/year
```

---

#### 3. Regional Performance Analysis

**Best vs Worst Performers:**

| Region | Revenue | Margin | Assessment |
|--------|---------|--------|------------|
| North Asia | $454K | **36.5%** | 🔥 Best margin |
| Central | $1.8M | 17.2% | ✅ High volume |
| Southeast Asia | $532K | **3.4%** | 🚨 Problem |
| Canada | $50K | 35.4% | 💎 Hidden gem |

**Key Insight:** North Asia generates 36% margins despite lower volume. Opportunity to scale.

---

#### 4. Category Profitability

**Winners & Losers:**

**Top Performers:**
- Copiers: $25K profit from just 5 sales
- Phones: $17K average per product line
- Accessories: Consistent 20%+ margins

**Bottom Performers:**
- Tables (Furniture): -$15K cumulative
- Machines: -$18K (3D printers killing category)
- Some storage products: negative margins

---

### 🛠️ Technical Implementation

#### Advanced SQL Queries

**Discount Impact Analysis:**
```sql
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
GROUP BY rango_descuento;
```

**Products with Losses:**
```sql
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
```

**Category Profitability (with CTEs):**
```sql
WITH categoria_stats AS (
    SELECT 
        category,
        sub_category,
        SUM(CAST(sales AS REAL)) as ventas,
        SUM(profit) as ganancia,
        (SUM(profit) / SUM(CAST(sales AS REAL))) * 100 as margen_pct
    FROM SuperStoreOrders
    GROUP BY category, sub_category
)
SELECT * FROM categoria_stats
ORDER BY ganancia DESC;
```

**Regional Analysis:**
```sql
SELECT 
    region,
    COUNT(DISTINCT customer_name) as clientes,
    ROUND(SUM(CAST(sales AS REAL)), 2) as ventas,
    ROUND(SUM(profit), 2) as profit,
    ROUND(SUM(profit) * 100.0 / SUM(CAST(sales AS REAL)), 2) as margen_pct
FROM SuperStoreOrders
GROUP BY region
ORDER BY ventas DESC;
```

---

### 📊 Dashboard Features

Interactive Streamlit dashboard with:

1. **Key Metrics**
   - Total sales
   - Total profit
   - Losses identified
   - Active markets

2. **Critical Alert: Discount Policy**
   - Visual breakdown by discount range
   - Loss calculation
   - Policy recommendations

3. **Discount Analysis**
   - Bar chart: profit by discount range
   - Table: detailed impact
   - Safe zone vs danger zone

4. **Loss-Making Products**
   - Horizontal bar chart (Top 10)
   - Category breakdown
   - Detailed loss table
   - Discontinuation recommendations

5. **Category Profitability**
   - Treemap visualization
   - Size = sales, color = margin
   - Top 5 vs Bottom 5 tables

6. **Logistics Efficiency**
   - Cost vs profit by shipping method
   - Dual-axis chart
   - Optimization opportunities

7. **Regional Performance**
   - Sunburst chart (Market → Region)
   - Top/Bottom performers
   - Expansion recommendations

---

### 🚀 Quick Start

#### Prerequisites
```bash
python >= 3.8
pip install streamlit pandas plotly
```

#### Setup Database

1. Download dataset: [Global SuperStore](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset)
2. Import to SQLite as `SuperStoreOrders`
3. Run queries from `queries/superstore_queries.sql`

#### Run Dashboard
```bash
cd 05-superstore-optimization
streamlit run superstore_dashboard.py
```

---

### 💼 Business Value

**Action Plan with ROI:**

| Priority | Action | Investment | Annual Savings | Payback |
|----------|--------|------------|----------------|---------|
| 🚨 URGENT | Discount policy (max 15%) | $0 | $80,000 | Immediate |
| 🚨 URGENT | Discontinue top 3 products | $5K | $26,000 | 2 months |
| ⚠️ SHORT | Review pricing (7 products) | $2K | $14,000 | 2 months |
| 🎯 MEDIUM | Expand North Asia | $50K | $90,000 | 7 months |
| 📦 MEDIUM | Optimize logistics | $20K | $30,000 | 8 months |

**TOTAL OPPORTUNITY: $210K/year savings**

**Investment Required: $77K**  
**Net Benefit Year 1: $133K**  
**ROI: 173%**

---

### 📈 Skills Demonstrated

**SQL:**
- ✅ CTEs (Common Table Expressions)
- ✅ Complex aggregations
- ✅ CASE statements for categorization
- ✅ Profitability analysis
- ✅ Multi-table queries

**Python/Streamlit:**
- ✅ Business intelligence dashboards
- ✅ Financial analysis
- ✅ Interactive visualizations (Plotly)
- ✅ Strategic recommendations

**Business Analysis:**
- ✅ Pricing strategy
- ✅ Product portfolio analysis
- ✅ Margin optimization
- ✅ KPI development
- ✅ ROI calculation
- ✅ Executive reporting

---

### 📸 Screenshots

![Dashboard Overview](screenshots/superstore-overview.png)
![Discount Analysis](screenshots/superstore-discounts.png)
![Product Losses](screenshots/superstore-losses.png)

---

### 📫 Contact

**José Granado**  
📧 [josegranadopass@gmail.com](mailto:josegranadopass@gmail.com)  
💼 [https://www.linkedin.com/in/perikogranado/](#)

---

## 🇪🇸 Español

### 📋 Resumen Ejecutivo

**Problema de Negocio:** Empresa retail con política de descuentos descontrolada destruyendo márgenes.

**Solución:** Análisis integral de rentabilidad usando SQL avanzado.

**Resultados:**
- 💰 **$210K/año** en ahorros identificados
- 🚨 **Descuentos >20%** generan margen -68%
- 📦 **$40K en pérdidas** de 10 productos
- 🎯 **58% precisión** en identificación

---

### 🔍 Hallazgos Clave

#### 1. Política de Descuentos Destructiva

**El Precipicio del Margen:**

| Rango | Margen Promedio | Estado |
|-------|-----------------|--------|
| Sin descuento | **+41%** | ✅ Saludable |
| 1-10% | **+30%** | ✅ Aceptable |
| 11-20% | **+16%** | ⚠️ Límite |
| 21-30% | **-8.7%** | 🚨 PÉRDIDA |
| >30% | **-68.8%** | 💀 CRÍTICO |

**Acción Recomendada:**
- Máximo descuento: 15%
- Aprobación gerencial para >10%
- Ahorro esperado: $80K/año

---

#### 2. Productos con Pérdidas

**Top 10 Productos Sangrando Dinero:**
- Cubify 3D Printer: -$8,880
- Lexmark Printer: -$4,590
- Motorola Phone: -$4,447
- **Total: -$40,072**

**Acciones:**
1. Descontinuar top 3
2. Aumentar precios resto
3. Auditar todos <5% margen

Recuperación: $40K/año

---

#### 3. Análisis Regional

**Mejores vs Peores:**
- North Asia: 36.5% margen (MEJOR)
- Southeast Asia: 3.4% margen (PROBLEMA)

---

#### 4. Rentabilidad por Categoría

**Ganadores:**
- Copiers: $25K de 5 ventas
- Phones: $17K promedio

**Perdedores:**
- Tables: -$15K acumulado
- Machines: -$18K (impresoras 3D)

---

### 💼 Valor de Negocio

**Plan de Acción con ROI:**

| Prioridad | Acción | Inversión | Ahorro Anual |
|-----------|--------|-----------|--------------|
| 🚨 URGENTE | Política descuentos | $0 | $80,000 |
| 🚨 URGENTE | Descontinuar top 3 | $5K | $26,000 |
| 🎯 MEDIO | Expandir North Asia | $50K | $90,000 |

**OPORTUNIDAD TOTAL: $210K/año**

---

### 📄 License

MIT License - Dataset from Kaggle (public)

---

*Part of [Data Analytics Portfolio](../README.md)*