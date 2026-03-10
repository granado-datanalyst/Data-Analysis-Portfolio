# 🎬 Top Series del Siglo XXI - Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

**Interactive analysis of the best series of the 21st century**

[📊 Live Demo](#) | [💻 Source Code](./app_series.py)

---

## 🇬🇧 English

### 📋 Project Overview

Interactive dashboard analyzing top TV series of the 21st century across multiple dimensions: rankings, genres, countries, streaming platforms, and awards.

**Problem:** Entertainment data scattered across multiple sources without integrated analysis.

**Solution:** Multi-tab dashboard with comprehensive trend analysis.

**Impact:** Complete visualization of streaming industry trends and patterns.

---

### ✨ Features

- **5 Interactive Tabs:**
  - 🏆 Rankings (Top series by score)
  - 🎭 Genres (Distribution and trends)
  - 🌍 Countries (Production by region)
  - 📺 Platforms (Streaming service analysis)
  - 🏅 Awards (Emmy nominations and wins)

- **Interactive Visualizations:**
  - Dynamic filtering
  - Plotly charts
  - Comparative analysis
  - Trend identification

---

### 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive charts
- **Excel** - Data source

---

### 🚀 Quick Start

#### Installation
```bash
# Clone repository
git clone https://github.com/tu-usuario/data-analytics-portfolio.git
cd 01-series-dashboard

# Install dependencies
pip install streamlit pandas plotly openpyxl

# Run dashboard
streamlit run app_series.py
```

#### Data Setup

The dashboard uses `TOP_SERIES_DEL_SIGLO_XXI.xlsx` with 5 sheets:
- Ranking
- Generos
- Paises
- Plataformas
- Premios

---

### 📊 Key Insights

- **Genre Distribution:** Drama dominates with 45% of top series
- **Platform Leaders:** HBO leads in quality content
- **Geographic Trends:** US and UK produce 70% of top-rated series
- **Awards Correlation:** Emmy nominations strongly correlate with viewer ratings

---

### 📸 Screenshots

![Dashboard Overview](screenshots/series-main.png)
![Genre Analysis](screenshots/series-genres.png)

---

### 💼 Business Value

**Use Cases:**
- Content strategy for streaming platforms
- Investment decisions for production companies
- Market trend analysis
- Competitive benchmarking

---

### 📫 Contact

**José Granado**  
📧 [josegranadopass@gmail.com](mailto:josegranadopass@gmail.com)  
💼 [https://www.linkedin.com/in/perikogranado/](#)

---

## 🇪🇸 Español

### 📋 Resumen del Proyecto

Dashboard interactivo que analiza las mejores series del siglo XXI en múltiples dimensiones: rankings, géneros, países, plataformas de streaming y premios.

**Problema:** Datos de entretenimiento dispersos sin análisis integrado.

**Solución:** Dashboard multi-pestaña con análisis completo de tendencias.

**Impacto:** Visualización completa de tendencias de la industria del streaming.

---

### ✨ Características

- **5 Pestañas Interactivas:**
  - 🏆 Rankings (Top series por puntuación)
  - 🎭 Géneros (Distribución y tendencias)
  - 🌍 Países (Producción por región)
  - 📺 Plataformas (Análisis de servicios de streaming)
  - 🏅 Premios (Nominaciones y ganadores Emmy)

---

### 🚀 Inicio Rápido
```bash
pip install streamlit pandas plotly openpyxl
streamlit run app_series.py
```

---

### 📊 Insights Clave

- **Distribución de Géneros:** Drama domina con 45% de las series top
- **Plataformas Líderes:** HBO lidera en contenido de calidad
- **Tendencias Geográficas:** US y UK producen el 70% de las series mejor valoradas
- **Correlación Premios:** Nominaciones Emmy correlacionan fuertemente con ratings

---

### 📄 License

MIT License - Data from public sources

---

*Part of [Data Analytics Portfolio](../README.md)*