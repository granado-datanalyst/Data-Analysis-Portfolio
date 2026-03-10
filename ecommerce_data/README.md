# 🇧🇷 Brazil E-commerce - Expansion Strategy

![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Geospatial](https://img.shields.io/badge/Geospatial-Analysis-green?style=flat)

**Strategic market analysis identifying 96% churn rate and expansion opportunities**

[📊 Live Demo](#) | [💻 Dashboard Code](ecommerceolist_dashboard_bilingual.py) | [🗃️ SQL Queries](ecommerce_olist_queries.sql)

---

## 🇬🇧 English

### 📋 Executive Summary

**Business Problem:** Brazilian e-commerce company facing 96% customer churn rate and dangerous geographic concentration (68% revenue in Southeast).

**Solution:** Comprehensive geospatial and customer behavior analysis across 96,096 customers to identify retention issues and expansion opportunities.

**Results:**
- 🚨 **96% churn rate** identified (customers only buy once)
- 🎯 **Northeastern Brazil** identified as untapped market
- 📈 **+4,500 customers** potential with expansion strategy
- 💰 **5x ROI** estimated on expansion investment

---

### 🔍 Key Findings

#### 1. Critical Retention Problem

**The 96% Churn Crisis:**
- 96% of customers make **only 1 purchase**
- Only 4% return for second purchase
- Average purchases per customer: **1.04**

**Root Cause:** No retention strategy, no loyalty program, no post-purchase engagement.

**Recommended Actions:**
```
Priority 1: Email marketing (day 7, 14, 30)
Priority 2: 10% discount on 2nd purchase
Priority 3: Points/rewards program
Expected Impact: +R$500K-1M/year
```

---

#### 2. Geographic Concentration Risk

**Current Distribution:**

| Region | Customers | % of Total | Risk Level |
|--------|-----------|------------|------------|
| Southeast (SP, RJ, MG) | 65,909 | 68.6% | 🚨 High |
| South | 13,693 | 14.2% | ⚠️ Medium |
| Northeast | 9,143 | 9.5% | ✅ Opportunity |
| Center-West | 5,597 | 5.8% | ⚠️ Medium |
| North | 1,794 | 1.9% | 🚨 Very Low |

**Risk:** 68% of revenue dependent on 3 states.

---

#### 3. Northeastern Expansion Opportunity

**Market Analysis:**

**Current Situation:**
- Northeast has 57M population
- Only 9.5% market penetration
- Major cities: Salvador (2.9M), Recife (1.7M), Fortaleza (2.7M)

**Opportunity:**
- **Gap vs Southeast:** 7.2x fewer customers per capita
- **Less competition** than saturated Southeast
- **Growing middle class** in the region

**Expansion Plan:**
```
Phase 1: Launch in Salvador (BA) and Recife (PE)
Phase 2: Free shipping for first 6 months
Phase 3: Localized marketing campaigns
Phase 4: Regional distribution center

Expected Results:
- +4,500 customers in Year 1
- 5x ROI
- 40% reduction in geographic risk
```

---

### 🛠️ Technical Implementation

#### Advanced SQL Queries

**Geographic Segmentation:**
```sql
WITH regiones AS (
    SELECT 
        customer_state,
        COUNT(DISTINCT customer_unique_id) as clientes_unicos,
        CASE 
            WHEN customer_state IN ('SP','RJ','MG','ES') THEN 'Sudeste'
            WHEN customer_state IN ('BA','SE','AL','PE','PB','RN','CE','PI','MA') THEN 'Noreste'
            WHEN customer_state IN ('RS','SC','PR') THEN 'Sur'
            WHEN customer_state IN ('MT','MS','GO','DF') THEN 'Centro-Oeste'
            WHEN customer_state IN ('AM','RR','AP','PA','TO','RO','AC') THEN 'Norte'
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
```

**Retention Analysis:**
```sql
SELECT 
    customer_state,
    COUNT(DISTINCT customer_unique_id) as clientes_unicos,
    COUNT(*) as total_registros,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT customer_unique_id), 2) as compras_promedio
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY clientes_unicos DESC;
```

**Logistic Optimization (ZIP Analysis):**
```sql
SELECT 
    customer_zip_code_prefix as zip_prefix,
    customer_city,
    COUNT(customer_id) as densidad
FROM olist_customers_dataset
GROUP BY customer_zip_code_prefix
HAVING densidad > 50
ORDER BY densidad DESC;
```

---

### 📊 Dashboard Features

Interactive Streamlit dashboard with:

1. **Security Metrics**
   - Total customers analyzed
   - Active states
   - Churn rate (96%)
   - Southeast concentration

2. **Critical Alert: Retention**
   - Visual pie chart (96% vs 4%)
   - Business impact calculation
   - Recommended actions

3. **Geographic Concentration**
   - Bar chart by state (Top 15)
   - Heat map visualization
   - Risk assessment

4. **Retention Analysis**
   - Stacked bar: 1 purchase vs 2+
   - Frequency distribution table
   - Customer lifetime value

5. **Expansion Strategy**
   - Southeast vs Northeast comparison
   - Opportunity sizing
   - ROI calculator

6. **Top Cities**
   - Volume by city
   - State breakdown
   - Expansion priorities

7. **Logistic Analysis (ZIP)**
   - Density by postal code
   - Distribution center recommendations
   - Last-mile optimization

---

### 🚀 Quick Start

#### Prerequisites
```bash
python >= 3.8
pip install streamlit pandas plotly
```

#### Setup Database

1. Download dataset: [Olist Brazilian E-commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Import `olist_customers_dataset.csv` to SQLite
3. Run queries from `queries/brasil_queries.sql`

#### Run Dashboard
```bash
cd 04-brazil-ecommerce
streamlit run brasil_dashboard.py
```

---

### 💼 Business Value

**Strategic Recommendations:**

| Priority | Action | Investment | Expected Return | Timeline |
|----------|--------|------------|-----------------|----------|
| 🚨 URGENT | Retention program | R$50K | R$500K-1M/year | 1 month |
| ✅ HIGH | Northeast expansion | R$200K | 5x ROI | 3 months |
| 📦 MEDIUM | Logistics optimization | R$100K | 15-20% cost ↓ | 6 months |

**Total Potential Impact:** R$2-3M additional annual revenue

---

### 📈 Skills Demonstrated

**SQL:**
- ✅ Geospatial analysis
- ✅ Customer segmentation
- ✅ Cohort analysis
- ✅ CTEs for complex calculations
- ✅ CASE statements for categorization

**Python/Streamlit:**
- ✅ Geographic visualizations
- ✅ Business intelligence dashboards
- ✅ Strategic recommendations
- ✅ ROI calculators

**Business Analysis:**
- ✅ Market opportunity assessment
- ✅ Churn analysis
- ✅ Geographic strategy
- ✅ Risk evaluation
- ✅ Financial modeling

---

### 📸 Screenshots

![Dashboard Overview](screenshots/brasil-overview.png)
![Churn Analysis](screenshots/brasil-churn.png)
![Expansion Strategy](screenshots/brasil-expansion.png)

---

### 📫 Contact

**José Granado**  
📧 [josegranadopass@gmail.com](mailto:josegranadopass@gmail.com)  
💼 [https://www.linkedin.com/in/perikogranado/](#)

---

## 🇪🇸 Español

### 📋 Resumen Ejecutivo

**Problema de Negocio:** E-commerce brasileño con 96% de churn y concentración geográfica peligrosa (68% en Sudeste).

**Solución:** Análisis geoespacial y de comportamiento de 96,096 clientes.

**Resultados:**
- 🚨 **96% de churn** identificado
- 🎯 **Noreste de Brasil** como mercado no explotado
- 📈 **+4,500 clientes** potenciales
- 💰 **ROI 5x** estimado

---

### 🔍 Hallazgos Clave

#### 1. Problema Crítico de Retención

**La Crisis del 96% Churn:**
- 96% de clientes compran **solo 1 vez**
- Solo 4% vuelve para segunda compra
- Promedio: **1.04 compras/cliente**

**Acciones Recomendadas:**
- Email marketing (día 7, 14, 30)
- 10% descuento en 2da compra
- Programa de puntos
- Impacto: +R$500K-1M/año

---

#### 2. Concentración Geográfica

**Distribución Actual:**
- Sudeste: 68.6% (RIESGO ALTO)
- Sur: 14.2%
- Noreste: 9.5% (OPORTUNIDAD)

---

#### 3. Oportunidad de Expansión al Noreste

**Análisis de Mercado:**
- Población: 57M habitantes
- Penetración actual: 9.5%
- Ciudades clave: Salvador, Recife, Fortaleza

**Plan de Expansión:**
```
Fase 1: Lanzamiento en Salvador y Recife
Fase 2: Envío gratis 6 meses
Fase 3: Campañas localizadas
Fase 4: Centro de distribución regional

Resultados Esperados:
- +4,500 clientes Año 1
- ROI 5x
- Reducción 40% riesgo geográfico
```

---

### 🛠️ Implementación Técnica

**Queries SQL Avanzadas:**
- Segmentación geográfica
- Análisis de retención
- Optimización logística

---

### 💼 Valor de Negocio

**Recomendaciones Estratégicas:**

| Prioridad | Acción | Inversión | Retorno | Plazo |
|-----------|--------|-----------|---------|-------|
| 🚨 URGENTE | Programa retención | R$50K | R$500K-1M/año | 1 mes |
| ✅ ALTA | Expansión Noreste | R$200K | 5x ROI | 3 meses |

**Impacto Total:** R$2-3M adicionales/año

---

### 📄 License

MIT License - Dataset from Kaggle (public - Olist)

---

*Part of [Data Analytics Portfolio](../README.md)*