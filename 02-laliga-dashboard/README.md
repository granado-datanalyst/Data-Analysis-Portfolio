# ⚽ La Liga - Player Performance Analytics

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Sports Analytics](https://img.shields.io/badge/Sports-Analytics-brightgreen?style=flat)

**Interactive dashboard for La Liga player statistics and performance analysis**

[📊 Live Demo](#) | [💻 Source Code](./app_la_liga.py)

---

## 🇬🇧 English

### 📋 Project Overview

Interactive dashboard for analyzing 200+ La Liga players across multiple performance metrics with advanced comparison tools.

**Problem:** Manual comparison of player statistics across multiple data sources.

**Solution:** Unified dashboard with player comparison and performance visualization.

**Impact:** Reusable sports analytics tool for scouting and performance analysis.

---

### ✨ Features

- **Player Database:** 200+ top La Liga players
- **Multi-Metric Analysis:**
  - Goals, Assists, xG (Expected Goals)
  - Defensive stats
  - Passing accuracy
  - Physical performance
  
- **Interactive Comparisons:**
  - Side-by-side player comparison
  - Position-based filtering
  - Team-based analysis
  - Custom metric selection

---

### 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Interactive web framework
- **Pandas** - Data processing
- **Plotly** - Advanced visualizations
- **Excel (3 sheets)** - Multi-source data integration

---

### 🚀 Quick Start
```bash
# Install dependencies
pip install streamlit pandas plotly openpyxl

# Run dashboard
streamlit run app_la_liga.py
```

#### Data Structure

Dataset: `sofascore_top_200_main_stats.xlsx`
- Sheet 1: Player stats
- Sheet 2: Team data
- Sheet 3: Historical comparisons

---

### 📊 Key Insights

**Analysis Capabilities:**
- Top scorers by position
- Assist leaders
- Defensive performance rankings
- xG overperformers/underperformers
- Team-level aggregations

---

### 💼 Business Value

**Use Cases:**
- **Scouting:** Identify transfer targets based on metrics
- **Performance Analysis:** Compare players across positions
- **Team Strategy:** Analyze strengths and weaknesses
- **Fan Engagement:** Interactive stats for media

**Potential Clients:**
- Football clubs (scouting departments)
- Sports media companies
- Betting analytics firms
- Fantasy football platforms

---

### 📸 Screenshots

![Player Comparison](screenshots/laliga-comparison.png)
![Team Analysis](screenshots/laliga-teams.png)

---

### 📫 Contact

**José Granado**  
📧 [josegranadopass@gmail.com](mailto:josegranadopass@gmail.com)
https://www.linkedin.com/in/perikogranado/

---

## 🇪🇸 Español

### 📋 Resumen del Proyecto

Dashboard interactivo para analizar 200+ jugadores de La Liga con múltiples métricas de rendimiento y herramientas avanzadas de comparación.

**Problema:** Comparación manual de estadísticas de jugadores.

**Solución:** Dashboard unificado con comparación de jugadores y visualización de rendimiento.

**Impacto:** Herramienta reutilizable de análisis deportivo para scouting.

---

### ✨ Características

- **Base de Datos:** 200+ jugadores top de La Liga
- **Análisis Multi-Métrico:**
  - Goles, Asistencias, xG
  - Estadísticas defensivas
  - Precisión de pases
  - Rendimiento físico

---

### 💼 Valor de Negocio

**Casos de Uso:**
- **Scouting:** Identificar objetivos de transferencia
- **Análisis de Rendimiento:** Comparar jugadores
- **Estrategia de Equipo:** Analizar fortalezas
- **Engagement de Fans:** Stats interactivas

---

### 📄 License

MIT License

---

*Parte del [Portfolio de Análisis de Datos](../README.md)*