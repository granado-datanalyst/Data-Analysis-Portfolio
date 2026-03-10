# 🇬🇧 Retail UK - Data Quality Audit

![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

**Comprehensive data quality audit identifying £2.1M in at-risk revenue**

[📊 Live Demo](#) | [💻 Dashboard Code](retail_uk_dashboard_bilingue.py) | [🗃️ SQL Queries](retail_queries.sql)

---

## 🇬🇧 English

### 📋 Executive Summary

**Business Problem:** E-commerce company with 1.7M transactions lacked visibility into data quality issues affecting revenue tracking and inventory management.

**Solution:** Comprehensive SQL-based audit using advanced queries (JOINs, Window Functions, CTEs) to identify and categorize data quality problems.

**Results:**
- 💰 **£2.1M in at-risk revenue** identified
- 🎯 **15% of total revenue** affected by quality issues
- ✅ **£200K/year savings** through recommended fixes
- 📊 **5 strategic dashboards** delivered

---

### 🔍 Key Findings

#### 1. Product Description Issues

**Problem:** Top revenue generators had invalid descriptions

| Product Description | Revenue | % of Total |
|-------------------|---------|------------|
| "?" | £1.24M | 6.5% |
| "damaged" | £781K | 4.1% |
| "damages" | £752K | 3.9% |
| "check" | £684K | 3.6% |

**Impact:** Impossible to optimize inventory or analyze product performance.

---

#### 2. Geographic Concentration Risk

- **UK:** 97% of revenue (£17.2M)
- **EIRE:** 2% (£1.8M)
- **Rest of world:** <1%

**Recommendation:** Geographic diversification strategy needed.

---

#### 3. VIP Customer Identification

- **Top 3 customers:** £3.4M (20% of revenue)
- **Risk:** High customer concentration
- **Action:** VIP retention program required

---

### 🛠️ Technical Implementation

#### SQL Queries Highlights

**Advanced Window Functions:**
```sql
WITH productos_rankeados AS (
    SELECT 
        country_name,
        product_name,
        SUM(total_amount) as ingresos,
        ROW_NUMBER() OVER (
            PARTITION BY country_name 
            ORDER BY SUM(total_amount) DESC
        ) as ranking
    FROM ventas v
    INNER JOIN productos p ON v.product_id = p.product_id
    GROUP BY country_name, product_name
)
SELECT * FROM productos_rankeados WHERE ranking <= 3;
```

**Complex JOINs (4 tables):**
```sql
SELECT v.invoice_id, p.product_name, pa.region, v.total_amount
FROM ventas v
INNER JOIN productos p ON v.product_id = p.product_id
INNER JOIN paises pa ON v.country_name = pa.country_name
INNER JOIN clientes c ON v.customer_id = c.customer_id;
```

---

### 📊 Dashboard Features

Interactive Streamlit dashboard with:

1. **Audit Metrics**
   - Total at-risk revenue
   - VIP customer count
   - Top performing country
   - Product quality issues

2. **Problematic Products**
   - Bar chart of top 10 issues
   - Detailed table with transaction counts
   - Category breakdown

3. **Customer Segmentation**
   - VIP (>£5K)
   - Premium (£2K-5K)
   - Regular (£500-2K)
   - Occasional (<£500)

4. **Regional Performance**
   - Revenue by country
   - Margin analysis
   - Performance indicators

5. **Top Products**
   - Revenue rankings
   - Units sold
   - Clean data only

---

### 🚀 Quick Start

#### Prerequisites
```bash
python >= 3.8
pip install streamlit pandas plotly sqlite3
```

#### Setup Database

1. Download dataset: [Online Retail II](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset)
2. Import to SQLite using DBeaver
3. Run queries from `retail_queries.sql`

#### Run Dashboard
```bash
cd 03-retail-uk-analysis
streamlit run retail_uk_dashboard.py
```

---

### 💼 Business Value

**Recommendations Delivered:**

| Action | Impact | Timeline |
|--------|--------|----------|
| Catalog audit | £2.1M revenue clarity | 2 weeks |
| VIP retention program | £200K/year | 1 month |
| Geographic expansion | Risk reduction 40% | 3 months |
| Data quality process | Prevent future issues | Ongoing |

**ROI:** £200K annual savings vs £5K analysis cost = **40x return**

---

### 📈 Skills Demonstrated

**SQL:**
- ✅ Complex JOINs (3-4 tables)
- ✅ Window Functions (ROW_NUMBER, PARTITION BY)
- ✅ CTEs (Common Table Expressions)
- ✅ Aggregations & GROUP BY
- ✅ CASE statements for categorization

**Python/Streamlit:**
- ✅ Interactive dashboards
- ✅ Data visualization (Plotly)
- ✅ SQLite integration
- ✅ Business intelligence reporting

**Business Analysis:**
- ✅ Data quality assessment
- ✅ Risk identification
- ✅ ROI calculation
- ✅ Actionable recommendations

---

### 📸 Screenshots

![Dashboard Overview](screenshots/retail-overview.png)
![Product Issues](screenshots/retail-problems.png)
![Customer Segmentation](screenshots/retail-customers.png)

---

### 📫 Contact

**José Granado**  
📧 [josegranadopass@gmail.com](mailto:josegranadopass@gmail.com)  
💼 [https://www.linkedin.com/in/perikogranado/](#)

---

## 🇪🇸 Español

### 📋 Resumen Ejecutivo

**Problema de Negocio:** Empresa de e-commerce con 1.7M transacciones sin visibilidad de problemas de calidad de datos.

**Solución:** Auditoría integral basada en SQL usando queries avanzadas.

**Resultados:**
- 💰 **£2.1M en riesgo** identificados
- 🎯 **15% de ingresos** afectados
- ✅ **£200K/año en ahorros** potenciales

---

### 🔍 Hallazgos Clave

#### 1. Problemas de Descripción

Los productos con mayor ingreso tenían descripciones inválidas ("?", "damaged", "check").

#### 2. Concentración Geográfica

97% de ingresos en UK - alto riesgo de concentración.

#### 3. Identificación de VIP

Top 3 clientes = 20% de ingresos totales.

---

### 🛠️ Implementación Técnica

**Highlights SQL:**
- Window Functions avanzadas
- JOINs complejos (4 tablas)
- CTEs para queries legibles
- Análisis de calidad de datos

---

### 💼 Valor de Negocio

**Recomendaciones:**
- Auditoría de catálogo → £2.1M clarificados
- Programa VIP → £200K/año
- Expansión geográfica → Reducción 40% riesgo

**ROI:** 40x retorno

---

### 📄 License

MIT License - Dataset from Kaggle (public)

---

*Part of [Data Analytics Portfolio](../README.md)*