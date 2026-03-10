import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# ============================================
st.set_page_config(
    page_title="Brasil E-commerce · Analytics",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# INICIALIZAR ESTADO (TEMA E IDIOMA)
# ============================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # 'dark' or 'light'

if 'language' not in st.session_state:
    st.session_state.language = 'en'  # 'en' or 'es'

# ============================================
# DICCIONARIO DE TEXTOS BILINGÜE
# ============================================
TEXTS = {
    'en': {
        # Header
        'title': '🇧🇷 Brazil E-commerce · Strategic Analysis',
        'subtitle': 'Analysis of 96,096 customers | Olist Store Dataset',
        'period': 'Analyzed period',
        
        # Metrics
        'total_customers': '👥 Total Customers',
        'active_states': '🗺️ Active States',
        'churn_rate': '⚠️ Churn Rate',
        'southeast_concentration': '🎯 Southeast Concentration',
        'coverage': 'coverage',
        'retention': 'retention',
        
        # Sidebar
        'language': '🌐 Language',
        'theme': '🎨 Theme',
        'dark_mode': '🌙 Dark Mode',
        'light_mode': '☀️ Light Mode',
        'global_filters': '🔍 Global Filters',
        'transactions': '📦 Transactions',
        'customers': '👥 Customers',
        'period_filter': '#### 📅 Period',
        'date_range': 'Date range',
        'states': '#### 🌍 States',
        'select_state': 'Select state',
        'all_states': 'All',
        'threshold': '#### 💰 Customer threshold',
        'show_states': 'Show states with customers >',
        'generate_report': '📥 Generate Report',
        'generating': 'Generating report...',
        'report_ready': 'Report generated! (Demo)',
        'updated': '● Data updated',
        'records': '● 96K records',
        'last_update': 'Last update:',
        
        # Tabs
        'tab_geography': '🗺️ Geography',
        'tab_retention': '👥 Retention',
        'tab_expansion': '🎯 Expansion',
        'tab_cities': '🏙️ Cities',
        'tab_logistics': '📦 Logistics',
        
        # Geography tab
        'geo_title': '### 🗺️ Geographic Concentration by State',
        'top_15_states': 'Top 15 States by Customer Count',
        'geo_insights': '### 💡 Geographic Insights',
        'top_3_states': '#### 📊 Top 3 States',
        'customers_count': 'customers',
        'total_concentration': '🎯 Top 3 Concentration',
        'high_concentration': '⚠️ High geographic dependency - Concentration risk',
        'healthy_distribution': '✅ Healthy geographic distribution',
        'top_10_states': '#### 📋 Top 10 States',
        
        # Retention tab
        'retention_title': '### 👥 Retention Analysis',
        'purchase_behavior': 'Purchase Behavior: One-time vs Recurring',
        'one_time': '1 purchase (Churn)',
        'recurring': '2+ purchases (Retention)',
        'number_of_customers': 'Number of Customers',
        'retention_funnel': 'Retention Funnel',
        'customers': 'Customers',
        'purchases': 'Number of Purchases',
        'view_full': '📊 View full distribution',
        
        # Expansion tab
        'expansion_title': '### 🎯 Expansion Opportunities',
        'strategic_distribution': 'Distribution by Strategic Category',
        'customers_by_category': 'Customers',
        'saturated_southeast': 'Saturated Region (Southeast)',
        'expansion_northeast': 'Expansion Region (Northeast)',
        'other_markets': 'Other Markets',
        'opportunity': '✅ OPPORTUNITY: NORTHEAST',
        'saturated': 'Saturated',
        'potential': 'Potential',
        'growth_gap': 'Growth gap',
        'northeast_population': 'Northeast population',
        'current_penetration': 'Current penetration',
        'strategy': '🎯 Strategy',
        'enter_salvador': 'Enter Salvador (BA) and Recife (PE)',
        'northeast_detail': '📍 Northeast States - Detail',
        'customers_detail': 'customers',
        
        # Cities tab
        'cities_title': '### 🏙️ Top Cities by Volume',
        'top_cities': 'Cities with Highest Concentration',
        'top_5_cities': '🔥 Top 5 Cities',
        'view_all_cities': '📋 View all cities',
        'city': 'City',
        'state': 'State',
        'customer_volume': 'Customer Volume',
        
        # Logistics tab
        'logistics_title': '### 📦 Logistics Analysis - ZIP Code Density',
        'logistics_info': '🎯 **Zones with >50 customers per ZIP code** - Candidates for distribution centers',
        'top_20_zips': 'Top 20 ZIP Codes by Density',
        'zip': 'ZIP',
        'customers_density': 'Customers',
        'logistics_opportunities': '🚚 Logistics Opportunities',
        'zones_identified': 'Zones identified',
        'highest_density': 'Highest density',
        'location': 'Location',
        'recommendation': 'Recommendation',
        'mini_hubs': 'Mini-hubs in top 5 ZIPs',
        'cost_reduction': 'Cost reduction: 15-20%',
        'same_day': 'Same-day delivery feasible',
        'top_15_zones': '🚚 Top 15 Zones for Distribution Centers',
        'zip_code': 'ZIP Code',
        'density': 'Density',
        
        # Strategic recommendations
        'strategic_recs': '### 💡 Strategic Recommendations',
        'urgent': '🚨 URGENT',
        'churn': 'Churn',
        'actions_urgent': ['Post-purchase email (day 7, 14, 30)', '10% discount on 2nd purchase', 'Loyalty program'],
        'roi': 'ROI: R$ 500K-1M/year',
        'opportunity': '✅ OPPORTUNITY',
        'northeast_expansion': 'Northeast Expansion',
        'actions_opportunity': ['Distribution center in Salvador', 'Digital marketing BA/PE/CE', 'Free shipping first 6 months'],
        'potential_customers': '+15K customers/year',
        'optimization': '🎯 OPTIMIZATION',
        'last_mile': 'Last Mile Logistics',
        'actions_optimization': ['Mini-hubs in high-density ZIPs', 'Same-day delivery in SP capital', 'Partnership with lockers'],
        'cost_savings': 'Cost reduction: 15-20%',
        
        # Footer
        'developed_by': 'Developed by José Granado with',
        'dataset': 'Dataset: Olist Store',
        'tools': 'Tools: SQL + Python + Streamlit',
        'rights': 'All rights reserved',
        
        # Tooltips
        'tooltip_total_customers': 'Unique customers in database',
        'tooltip_active_states': 'States with presence',
        'tooltip_churn': 'Customers who buy only once',
        'tooltip_concentration': '% of customers in SP, RJ, MG',
        'tooltip_date_range': 'Filter data by invoice date',
        'tooltip_state': 'Filter analysis by specific state',
    },
    'es': {
        # Header
        'title': '🇧🇷 Brasil E-commerce · Análisis Estratégico',
        'subtitle': 'Análisis de 96,096 clientes | Dataset Olist Store',
        'period': 'Período analizado',
        
        # Metrics
        'total_customers': '👥 Total Clientes',
        'active_states': '🗺️ Estados Activos',
        'churn_rate': '⚠️ Churn Rate',
        'southeast_concentration': '🎯 Concentración Sudeste',
        'coverage': 'cobertura',
        'retention': 'retención',
        
        # Sidebar
        'language': '🌐 Idioma',
        'theme': '🎨 Tema',
        'dark_mode': '🌙 Modo Oscuro',
        'light_mode': '☀️ Modo Claro',
        'global_filters': '🔍 Filtros Globales',
        'transactions': '📦 Transacciones',
        'customers': '👥 Clientes',
        'period_filter': '#### 📅 Período',
        'date_range': 'Rango de fechas',
        'states': '#### 🌍 Estados',
        'select_state': 'Seleccionar estado',
        'all_states': 'Todos',
        'threshold': '#### 💰 Umbral de clientes',
        'show_states': 'Mostrar estados con clientes >',
        'generate_report': '📥 Generar Reporte',
        'generating': 'Generando reporte...',
        'report_ready': '¡Reporte generado! (Demo)',
        'updated': '● Datos actualizados',
        'records': '● 96K registros',
        'last_update': 'Última actualización:',
        
        # Tabs
        'tab_geography': '🗺️ Geografía',
        'tab_retention': '👥 Retención',
        'tab_expansion': '🎯 Expansión',
        'tab_cities': '🏙️ Ciudades',
        'tab_logistics': '📦 Logística',
        
        # Geography tab
        'geo_title': '### 🗺️ Concentración Geográfica por Estado',
        'top_15_states': 'Top 15 Estados por Número de Clientes',
        'geo_insights': '### 💡 Insights Geográficos',
        'top_3_states': '#### 📊 Top 3 Estados',
        'customers_count': 'clientes',
        'total_concentration': '🎯 Concentración Top 3',
        'high_concentration': '⚠️ Alta dependencia geográfica - Riesgo de concentración',
        'healthy_distribution': '✅ Distribución geográfica saludable',
        'top_10_states': '#### 📋 Top 10 Estados',
        
        # Retention tab
        'retention_title': '### 👥 Análisis de Retención',
        'purchase_behavior': 'Comportamiento de Compra: Una vez vs Recurrente',
        'one_time': '1 compra (Churn)',
        'recurring': '2+ compras (Retención)',
        'number_of_customers': 'Número de Clientes',
        'retention_funnel': 'Funnel de Retención',
        'customers': 'Clientes',
        'purchases': 'Número de Compras',
        'view_full': '📊 Ver distribución completa',
        
        # Expansion tab
        'expansion_title': '### 🎯 Oportunidades de Expansión',
        'strategic_distribution': 'Distribución por Categoría Estratégica',
        'customers_by_category': 'Clientes',
        'saturated_southeast': 'Región Saturada (Sudeste)',
        'expansion_northeast': 'Región de Expansión (Noreste)',
        'other_markets': 'Otros Mercados',
        'opportunity': '✅ OPORTUNIDAD: NORESTE',
        'saturated': 'Saturado',
        'potential': 'Potencial',
        'growth_gap': 'GAP de crecimiento',
        'northeast_population': 'Población Noreste',
        'current_penetration': 'Penetración actual',
        'strategy': '🎯 Estrategia',
        'enter_salvador': 'Entrar en Salvador (BA) y Recife (PE)',
        'northeast_detail': '📍 Estados Noreste - Detalle',
        'customers_detail': 'clientes',
        
        # Cities tab
        'cities_title': '### 🏙️ Top Ciudades por Volumen',
        'top_cities': 'Ciudades con Mayor Concentración',
        'top_5_cities': '🔥 Top 5 Ciudades',
        'view_all_cities': '📋 Ver todas las ciudades',
        'city': 'Ciudad',
        'state': 'Estado',
        'customer_volume': 'Volumen de Clientes',
        
        # Logistics tab
        'logistics_title': '### 📦 Análisis Logístico - Densidad por Código Postal',
        'logistics_info': '🎯 **Zonas con >50 clientes por código postal** - Candidatas para centros de distribución',
        'top_20_zips': 'Top 20 Códigos Postales por Densidad',
        'zip': 'ZIP',
        'customers_density': 'Clientes',
        'logistics_opportunities': '🚚 Oportunidades Logísticas',
        'zones_identified': 'Zonas identificadas',
        'highest_density': 'Mayor densidad',
        'location': 'Ubicación',
        'recommendation': 'Recomendación',
        'mini_hubs': 'Mini-hubs en top 5 ZIPs',
        'cost_reduction': 'Reducción costos: 15-20%',
        'same_day': 'Entrega same-day factible',
        'top_15_zones': '🚚 Top 15 Zonas para Centros de Distribución',
        'zip_code': 'Código Postal',
        'density': 'Densidad',
        
        # Strategic recommendations
        'strategic_recs': '### 💡 Recomendaciones Estratégicas',
        'urgent': '🚨 URGENTE',
        'churn': 'Churn',
        'actions_urgent': ['Email post-compra (día 7, 14, 30)', 'Cupón 10% en 2da compra', 'Programa de puntos'],
        'roi': 'ROI: R$ 500K-1M/año',
        'opportunity': '✅ OPORTUNIDAD',
        'northeast_expansion': 'Expansión Noreste',
        'actions_opportunity': ['Centro distribución Salvador', 'Marketing digital BA/PE/CE', 'Free shipping primeros 6 meses'],
        'potential_customers': '+15K clientes/año',
        'optimization': '🎯 OPTIMIZACIÓN',
        'last_mile': 'Logística Última Milla',
        'actions_optimization': ['Mini-hubs en ZIPs de alta densidad', 'Entrega same-day en SP capital', 'Partnership con lockers'],
        'cost_savings': 'Reducción costos: 15-20%',
        
        # Footer
        'developed_by': 'Desarrollado por José Granado con',
        'dataset': 'Dataset: Olist Store',
        'tools': 'Herramientas: SQL + Python + Streamlit',
        'rights': 'Todos los derechos reservados',
        
        # Tooltips
        'tooltip_total_customers': 'Clientes únicos en la base',
        'tooltip_active_states': 'Estados con presencia',
        'tooltip_churn': 'Clientes que compran solo 1 vez',
        'tooltip_concentration': '% de clientes en SP, RJ, MG',
        'tooltip_date_range': 'Filtra los datos por fecha de factura',
        'tooltip_state': 'Filtra el análisis por estado específico',
    }
}

# Función helper para textos
def t(key):
    """Retorna texto en el idioma actual"""
    return TEXTS[st.session_state.language].get(key, key)

# ============================================
# PALETA DE COLORES (dinámica según tema)
# ============================================
COLORS = {
    'primary': '#8B5CF6',      # Morado (color DiSito)
    'secondary': '#F59E0B',     # Naranja
    'success': '#10B981',        # Verde
    'warning': '#EF4444',        # Rojo
    'info': '#3B82F6',           # Azul
    'background': '#0A0A0F' if st.session_state.theme == 'dark' else '#F8FAFC',
    'card_bg': '#1A1A23' if st.session_state.theme == 'dark' else '#FFFFFF',
    'text': '#FFFFFF' if st.session_state.theme == 'dark' else '#0F172A',
    'text_secondary': '#A0A0B0' if st.session_state.theme == 'dark' else '#475569',
    'border': '#2A2A35' if st.session_state.theme == 'dark' else '#E2E8F0',
}

# ============================================
# CSS personalizado
# ============================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {COLORS['background']};
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6, p, li, span, div {{
        color: {COLORS['text']} !important;
    }}
    
    .stMarkdown, .stText, .stCaption {{
        color: {COLORS['text']} !important;
    }}
    
    div[data-testid="stMetric"] {{
        background-color: {COLORS['card_bg']};
        padding: 1.5rem 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid {COLORS['border']};
        transition: transform 0.2s;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: {COLORS['primary']};
    }}
    
    div[data-testid="stMetric"] label {{
        color: {COLORS['text_secondary']} !important;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {COLORS['primary']} !important;
    }}
    
    .stButton button {{
        background-color: {COLORS['secondary']};
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }}
    
    .stButton button:hover {{
        background-color: #d47d00;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid {COLORS['border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        font-weight: 500;
        color: {COLORS['text_secondary']} !important;
        transition: all 0.2s;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {COLORS['primary']} !important;
        border-bottom-color: {COLORS['primary']} !important;
        border-bottom-width: 3px;
    }}
    
    .alert-card {{
        background-color: {COLORS['card_bg']};
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 4px solid;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid {COLORS['border']};
    }}
    
    .alert-card.warning {{ border-left-color: {COLORS['warning']}; }}
    .alert-card.success {{ border-left-color: {COLORS['success']}; }}
    .alert-card.info {{ border-left-color: {COLORS['info']}; }}
    
    .custom-divider {{
        height: 2px;
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 50%, transparent 100%);
        margin: 2rem 0;
        opacity: 0.2;
    }}
    
    .insight-box {{
        background-color: {COLORS['card_bg']};
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 1px solid {COLORS['border']};
    }}
    
    .progress-bar-bg {{
        background-color: {COLORS['text_secondary']}20;
        height: 8px;
        border-radius: 4px;
        margin: 0.3rem 0;
    }}
    
    .progress-bar-fill {{
        height: 8px;
        border-radius: 4px;
        background-color: {COLORS['primary']};
    }}
    
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }}
    
    .badge-success {{
        background-color: rgba(16, 185, 129, 0.1);
        color: {COLORS['success']} !important;
        border: 1px solid {COLORS['success']}40;
    }}
    
    .badge-warning {{
        background-color: rgba(239, 68, 68, 0.1);
        color: {COLORS['warning']} !important;
        border: 1px solid {COLORS['warning']}40;
    }}
    
    .badge-info {{
        background-color: rgba(59, 130, 246, 0.1);
        color: {COLORS['info']} !important;
        border: 1px solid {COLORS['info']}40;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE CARGA
# ============================================

@st.cache_data(ttl=3600, show_spinner="🔄 Cargando datos de Brasil...")
def load_all_tables(db_path):
    """Carga todas las tablas de una vez"""
    
    tables = [
        "df_brasil_geografia",
        "df_brasil_retencion", 
        "df_brasil_expansion",
        "df_brasil_top_ciudades",
        "df_brasil_logistica"
    ]
    
    data = {}
    
    try:
        with sqlite3.connect(db_path) as conn:
            for table in tables:
                cursor = conn.cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
                if cursor.fetchone():
                    data[table] = pd.read_sql_query(f"SELECT * FROM [{table}]", conn)
                else:
                    st.warning(f"⚠️ Tabla no encontrada: {table}")
                    data[table] = pd.DataFrame()
        
        return data
        
    except sqlite3.Error as e:
        st.error(f"❌ Error de base de datos: {e}")
        return {}
    except Exception as e:
        st.error(f"❌ Error inesperado: {e}")
        return {}

# ============================================
# CARGA DE DATOS
# ============================================

DB_PATH = r"C:\Users\JOSE GRANADO PC\desktop\ecommerce_data\ecommerceolist.db"

with st.spinner("🔄 Conectando a la base de datos..."):
    data = load_all_tables(DB_PATH)

if not data:
    st.error("❌ No se pudo cargar ningún dato. Verifica la conexión.")
    st.stop()

df_geografia = data.get("df_brasil_geografia", pd.DataFrame())
df_retencion = data.get("df_brasil_retencion", pd.DataFrame())
df_expansion = data.get("df_brasil_expansion", pd.DataFrame())
df_ciudades = data.get("df_brasil_top_ciudades", pd.DataFrame())
df_logistica = data.get("df_brasil_logistica", pd.DataFrame())

if df_geografia.empty:
    st.error("❌ Tabla de geografía vacía. Verifica la base de datos.")
    st.stop()

# ============================================
# HEADER Y SIDEBAR
# ============================================

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: {COLORS['primary']};">📊 Brasil E-commerce</h2>
        <p style="color: {COLORS['text_secondary']};">Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== SELECTOR DE IDIOMA =====
    st.markdown(f"### {t('language')}")
    col_lang1, col_lang2 = st.columns(2)
    with col_lang1:
        if st.button("🇬🇧 English", use_container_width=True, 
                    type="primary" if st.session_state.language == 'en' else "secondary"):
            st.session_state.language = 'en'
            st.rerun()
    with col_lang2:
        if st.button("🇪🇸 Español", use_container_width=True,
                    type="primary" if st.session_state.language == 'es' else "secondary"):
            st.session_state.language = 'es'
            st.rerun()
    
    st.markdown("---")
    
    # ===== SELECTOR DE TEMA =====
    st.markdown(f"### {t('theme')}")
    tema_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    tema_text = t('dark_mode') if st.session_state.theme == 'light' else t('light_mode')
    
    if st.button(f"{tema_icon} {tema_text}", use_container_width=True):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.rerun()
    
    st.markdown("---")
    
    st.markdown(f"### {t('global_filters')}")
    
    # Métricas de resumen en sidebar
    st.markdown(f"""
    <div style="background: {COLORS['background']}; padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid {COLORS['border']};">
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem;">{t('transactions')}</p>
        <p style="margin: 0; font-size: 1.3rem; font-weight: 700; color: {COLORS['primary']};">{df_geografia['total_clientes'].sum():,}</p>
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem; margin-top: 0.5rem;">{t('customers')}</p>
        <p style="margin: 0; font-size: 1.1rem; color: {COLORS['info']};">{df_geografia['total_clientes'].sum():,}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# HEADER PRINCIPAL
# ============================================

col_title, col_toggle = st.columns([4, 1])

with col_title:
    st.markdown(f"""
    <h1 style="color: {COLORS['primary']};">{t('title')}</h1>
    <p style="color: {COLORS['text_secondary']};">{t('subtitle')}</p>
    """, unsafe_allow_html=True)

with col_toggle:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: {COLORS['card_bg']}; padding: 0.5rem; border-radius: 12px; text-align: center; border: 1px solid {COLORS['border']};">
        <p style="margin: 0; color: {COLORS['text']};">{t('period')}</p>
        <p style="margin: 0; color: {COLORS['primary']}; font-weight: 600;">{datetime.now().strftime('%Y')}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# MÉTRICAS PRINCIPALES
# ============================================

st.markdown(f"<h3 style='color: {COLORS['text']};'>📊 {t('total_customers')}</h3>", unsafe_allow_html=True)

total_clientes = df_geografia['total_clientes'].sum() if not df_geografia.empty else 0
estados_activos = len(df_geografia) if not df_geografia.empty else 0

if not df_retencion.empty:
    clientes_1_compra = df_retencion[df_retencion['compras_realizadas'] == 1]['total_usuarios'].sum()
    total_retencion = df_retencion['total_usuarios'].sum()
    tasa_churn = (clientes_1_compra / total_retencion * 100) if total_retencion > 0 else 0
else:
    clientes_1_compra = 0
    total_retencion = 0
    tasa_churn = 0

if not df_expansion.empty:
    sudeste = df_expansion[df_expansion['categoria_estrategica'] == 'Región Saturada (Sudeste)']['clientes'].sum()
    pct_sudeste = (sudeste / total_clientes * 100) if total_clientes > 0 else 0
else:
    sudeste = 0
    pct_sudeste = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        t('total_customers'),
        f"{total_clientes:,}",
        help=t('tooltip_total_customers')
    )

with col2:
    st.metric(
        t('active_states'),
        f"{estados_activos}/27",
        delta=f"{estados_activos/27*100:.0f}% {t('coverage')}",
        help=t('tooltip_active_states')
    )

with col3:
    st.metric(
        t('churn_rate'),
        f"{tasa_churn:.1f}%",
        delta=f"{100-tasa_churn:.1f}% {t('retention')}",
        delta_color="inverse",
        help=t('tooltip_churn')
    )

with col4:
    st.metric(
        t('southeast_concentration'),
        f"{pct_sudeste:.1f}%",
        help=t('tooltip_concentration')
    )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# ALERTA CRÍTICA
# ============================================

col_alert1, col_alert2 = st.columns([2, 1])

with col_alert1:
    st.markdown(f"""
    <div class="alert-card warning">
        <h3 style="color: {COLORS['warning']};">🚨 {t('urgent')}: {t('churn_rate')}</h3>
        <p style="font-size: 2.5rem; font-weight: 700; margin: 0;">{tasa_churn:.1f}%</p>
        <p style="color: {COLORS['text_secondary']};">{t('one_time')}</p>
        <hr style="border: none; border-top: 1px solid {COLORS['border']};">
        <p><strong>📊 {t('customers')}:</strong></p>
        <ul>
            <li>{t('recurring')}: <strong>{100-tasa_churn:.1f}%</strong></li>
            <li>{t('one_time')}: <strong>{clientes_1_compra:,}</strong></li>
            <li>{t('roi')}</li>
        </ul>
        <p style="background: {COLORS['warning']}20; padding: 0.5rem; border-radius: 8px;">
            <strong>🎯 {t('strategy')}:</strong> {', '.join(TEXTS[st.session_state.language]['actions_urgent'])}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_alert2:
    if not df_retencion.empty and total_retencion > 0:
        fig_ret_mini = px.pie(
            values=[clientes_1_compra, total_retencion - clientes_1_compra],
            names=[t('one_time'), t('recurring')],
            title=t('churn_rate'),
            color_discrete_sequence=[COLORS['warning'], COLORS['success']],
            hole=0.5
        )
        fig_ret_mini.update_layout(
            height=300,
            showlegend=True,
            margin=dict(t=40, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        st.plotly_chart(fig_ret_mini, use_container_width=True)
    else:
        st.info("No hay datos de retención disponibles")

# ============================================
# TABS
# ============================================

tab_geo, tab_ret, tab_exp, tab_cities, tab_log = st.tabs([
    t('tab_geography'),
    t('tab_retention'), 
    t('tab_expansion'),
    t('tab_cities'),
    t('tab_logistics')
])

# ============================================
# TAB 1: GEOGRAFÍA
# ============================================

with tab_geo:
    st.markdown(t('geo_title'))
    
    col_geo1, col_geo2 = st.columns([2, 1])
    
    with col_geo1:
        if not df_geografia.empty:
            fig1 = px.bar(
                df_geografia.head(15),
                x='total_clientes',
                y='estado',
                orientation='h',
                title=t('top_15_states'),
                labels={'total_clientes': t('customers'), 'estado': ''},
                color='total_clientes',
                color_continuous_scale='Blues',
                text='total_clientes'
            )
            
            fig1.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig1.update_layout(
                showlegend=False,
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis={'categoryorder': 'total ascending'},
                font=dict(color=COLORS['text'])
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col_geo2:
        st.markdown(t('geo_insights'))
        
        if not df_geografia.empty and len(df_geografia) >= 3:
            top3_estados = df_geografia.head(3)
            top3_clientes = top3_estados['total_clientes'].sum()
            pct_top3 = (top3_clientes / total_clientes * 100) if total_clientes > 0 else 0
            
            st.markdown(t('top_3_states'))
            
            for i in range(3):
                st.markdown(f"**{i+1}. {top3_estados.iloc[i]['estado']}**")
                col_bar, col_pct = st.columns([3, 1])
                with col_bar:
                    st.progress(top3_estados.iloc[i]['total_clientes']/total_clientes)
                with col_pct:
                    st.write(f"{top3_estados.iloc[i]['total_clientes']/total_clientes*100:.1f}%")
                st.caption(f"{top3_estados.iloc[i]['total_clientes']:,} {t('customers_count')}")
            
            st.divider()
            
            st.metric(
                t('total_concentration'),
                f"{pct_top3:.1f}%",
                help=t('tooltip_concentration')
            )
            
            if pct_top3 > 50:
                st.warning(t('high_concentration'))
            else:
                st.success(t('healthy_distribution'))
            
            st.divider()
            
            st.markdown(t('top_10_states'))
            geo_display = df_geografia.head(10).copy()
            geo_display.columns = ['Estado', 'Clientes', 'Ciudades']
            st.dataframe(
                geo_display,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Clientes": st.column_config.NumberColumn(format="%d")
                }
            )
        else:
            st.info("No hay suficientes datos geográficos")

# ============================================
# TAB 2: RETENCIÓN
# ============================================

with tab_ret:
    st.markdown(f"<h3 style='color: {COLORS['text']};'>{t('retention_title')}</h3>", unsafe_allow_html=True)
    
    if not df_retencion.empty and total_retencion > 0:
        col_ret1, col_ret2 = st.columns([1, 1])
        
        with col_ret1:
            fig2 = go.Figure()
            
            usuarios_1_compra = df_retencion[df_retencion['compras_realizadas'] == 1]['total_usuarios'].values[0]
            usuarios_2plus = total_retencion - usuarios_1_compra
            
            fig2.add_trace(go.Bar(
                x=['Clientes'],
                y=[usuarios_1_compra],
                name=t('one_time'),
                marker_color=COLORS['warning'],
                text=[f'{usuarios_1_compra:,}<br>({tasa_churn:.1f}%)'],
                textposition='inside',
                textfont=dict(size=14, color='white')
            ))
            
            fig2.add_trace(go.Bar(
                x=['Clientes'],
                y=[usuarios_2plus],
                name=t('recurring'),
                marker_color=COLORS['success'],
                text=[f'{usuarios_2plus:,}<br>({100-tasa_churn:.1f}%)'],
                textposition='inside',
                textfont=dict(size=14, color='white')
            ))
            
            fig2.update_layout(
                title=t('purchase_behavior'),
                barmode='stack',
                height=400,
                yaxis_title=t('number_of_customers'),
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'])
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        with col_ret2:
            compras_counts = df_retencion.sort_values('compras_realizadas').head(10)
            
            fig_funnel = px.funnel(
                compras_counts,
                x='total_usuarios',
                y='compras_realizadas',
                title=t('retention_funnel'),
                labels={'total_usuarios': t('customers'), 'compras_realizadas': t('purchases')}
            )
            
            fig_funnel.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'])
            )
            
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with st.expander(t('view_full')):
            st.dataframe(
                df_retencion.rename(columns={
                    'compras_realizadas': t('purchases'),
                    'total_usuarios': t('customers')
                }),
                hide_index=True,
                use_container_width=True
            )
    else:
        st.info("No hay datos de retención disponibles")

# ============================================
# TAB 3: EXPANSIÓN
# ============================================

with tab_exp:
    st.markdown(f"<h3 style='color: {COLORS['text']};'>{t('expansion_title')}</h3>", unsafe_allow_html=True)
    
    if not df_expansion.empty:
        expansion_grouped = df_expansion.groupby('categoria_estrategica')['clientes'].sum().reset_index()
        expansion_grouped = expansion_grouped.sort_values('clientes', ascending=False)
        
        col_exp1, col_exp2 = st.columns([2, 1])
        
        with col_exp1:
            fig3 = px.bar(
                expansion_grouped,
                x='categoria_estrategica',
                y='clientes',
                title=t('strategic_distribution'),
                labels={'clientes': t('customers_by_category'), 'categoria_estrategica': ''},
                color='categoria_estrategica',
                color_discrete_map={
                    'Región Saturada (Sudeste)': COLORS['warning'],
                    'Región de Expansión (Noreste)': COLORS['success'],
                    'Otros Mercados': '#95a5a6'
                },
                text='clientes'
            )
            
            fig3.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig3.update_layout(
                showlegend=False,
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text'])
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_exp2:
            sudeste_clientes = expansion_grouped[expansion_grouped['categoria_estrategica'] == 'Región Saturada (Sudeste)']['clientes'].values[0] if any(expansion_grouped['categoria_estrategica'] == 'Región Saturada (Sudeste)') else 0
            noreste_clientes = expansion_grouped[expansion_grouped['categoria_estrategica'] == 'Región de Expansión (Noreste)']['clientes'].values[0] if any(expansion_grouped['categoria_estrategica'] == 'Región de Expansión (Noreste)') else 0
            
            st.markdown(f"""
            <div class="alert-card success">
                <h4 style="color: {COLORS['success']};">{t('opportunity')}</h4>
                <p><strong>{t('saturated')}:</strong> {sudeste_clientes:,} {t('customers_count')}</p>
                <p><strong>{t('potential')}:</strong> {noreste_clientes:,} {t('customers_count')}</p>
                <hr style="border: none; border-top: 1px solid {COLORS['border']};">
                <p><strong>{t('growth_gap')}:</strong> {((sudeste_clientes/noreste_clientes)-1)*100:.0f}%</p>
                <p><strong>{t('northeast_population')}:</strong> 57M</p>
                <p><strong>{t('current_penetration')}:</strong> {(noreste_clientes/57000000)*100:.3f}%</p>
                <p style="margin-top: 1rem;"><strong>{t('strategy')}:</strong> {t('enter_salvador')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='color: {COLORS['text']};'>{t('northeast_detail')}</h4>", unsafe_allow_html=True)
        estados_noreste = df_expansion[
            df_expansion['categoria_estrategica'] == 'Región de Expansión (Noreste)'
        ].sort_values('clientes', ascending=False)
        
        for idx, row in estados_noreste.iterrows():
            st.markdown(f"""
            <div class="insight-box">
                <span style="font-weight: 600;">{row['customer_state']}</span>
                <span style="float: right; color: {COLORS['success']};">{row['clientes']:,} {t('customers_detail')}</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 4: CIUDADES
# ============================================

with tab_cities:
    st.markdown(f"<h3 style='color: {COLORS['text']};'>{t('cities_title')}</h3>", unsafe_allow_html=True)
    
    if not df_ciudades.empty:
        col_city1, col_city2 = st.columns([2, 1])
        
        with col_city1:
            fig4 = px.bar(
                df_ciudades,
                x='volumen_clientes',
                y='customer_city',
                orientation='h',
                title=t('top_cities'),
                labels={'volumen_clientes': t('customers'), 'customer_city': ''},
                color='customer_state',
                text='volumen_clientes',
                hover_data=['customer_state']
            )
            
            fig4.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig4.update_layout(
                height=600,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with col_city2:
            st.markdown(f"<h4 style='color: {COLORS['text']};'>{t('top_5_cities')}</h4>", unsafe_allow_html=True)
            
            for i, (idx, row) in enumerate(df_ciudades.head(5).iterrows()):
                st.markdown(f"""
                <div class="insight-box">
                    <span style="font-size: 1.2rem;">#{i+1}</span>
                    <span style="font-weight: 600; margin-left: 0.5rem;">{row['customer_city']}</span>
                    <span style="float: right; color: {COLORS['primary']}; font-weight: 600;">{row['volumen_clientes']:,}</span>
                    <div style="font-size: 0.8rem; color: {COLORS['text_secondary']};">{row['customer_state']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander(t('view_all_cities')):
            ciudades_display = df_ciudades.copy()
            ciudades_display.columns = [t('city'), t('state'), t('customer_volume')]
            st.dataframe(
                ciudades_display.style.format({t('customer_volume'): '{:,.0f}'}),
                hide_index=True,
                use_container_width=True
            )

# ============================================
# TAB 5: LOGÍSTICA
# ============================================

with tab_log:
    st.markdown(f"<h3 style='color: {COLORS['text']};'>{t('logistics_title')}</h3>", unsafe_allow_html=True)
    
    if not df_logistica.empty:
        st.info(t('logistics_info'))
        
        df_logistica_top = df_logistica.head(20).copy()
        df_logistica_top['zip_label'] = df_logistica_top['zip_prefix'].astype(str) + ' - ' + df_logistica_top['customer_city']
        
        col_log1, col_log2 = st.columns([2, 1])
        
        with col_log1:
            fig5 = px.bar(
                df_logistica_top.sort_values('densidad'),
                x='densidad',
                y='zip_label',
                orientation='h',
                title=t('top_20_zips'),
                labels={'densidad': t('customers_density'), 'zip_label': ''},
                color='densidad',
                color_continuous_scale='Teal',
                text='densidad'
            )
            
            fig5.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig5.update_layout(
                showlegend=False,
                height=700,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLORS['text']),
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        with col_log2:
            total_zonas = len(df_logistica)
            max_densidad = df_logistica['densidad'].max()
            ciudad_max = df_logistica[df_logistica['densidad'] == max_densidad]['customer_city'].values[0]
            zip_max = df_logistica[df_logistica['densidad'] == max_densidad]['zip_prefix'].values[0]
            
            st.markdown(f"""
            <div class="alert-card info">
                <h4 style="color: {COLORS['info']};">{t('logistics_opportunities')}</h4>
                <p><strong>{t('zones_identified')}:</strong> {total_zonas}</p>
                <p><strong>{t('highest_density')}:</strong> {max_densidad:,} {t('customers_count')}</p>
                <p><strong>{t('location')}:</strong> {ciudad_max} ({t('zip')}: {zip_max})</p>
                <hr style="border: none; border-top: 1px solid {COLORS['border']};">
                <p><strong>{t('recommendation')}:</strong></p>
                <ul>
                    <li>{t('mini_hubs')}</li>
                    <li>{t('cost_reduction')}</li>
                    <li>{t('same_day')}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<h4 style='color: {COLORS['text']};'>{t('top_15_zones')}</h4>", unsafe_allow_html=True)
        logistica_display = df_logistica.head(15).copy()
        logistica_display['zip_prefix'] = logistica_display['zip_prefix'].astype(str)
        logistica_display.columns = [t('zip_code'), t('city'), t('density')]
        
        st.dataframe(
            logistica_display.style.background_gradient(
                subset=[t('density')],
                cmap='Greens'
            ),
            hide_index=True, 
            use_container_width=True
        )

# ============================================
# RECOMENDACIONES ESTRATÉGICAS
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: {COLORS['text']};'>{t('strategic_recs')}</h3>", unsafe_allow_html=True)

col_rec1, col_rec2, col_rec3 = st.columns(3)

with col_rec1:
    st.markdown(f"""
    <div class="alert-card warning">
        <h4 style="color: {COLORS['warning']};">{t('urgent')}</h4>
        <p><strong>{t('churn')} {tasa_churn:.1f}%</strong></p>
        <ul style="color: {COLORS['text_secondary']};">
            <li>{TEXTS[st.session_state.language]['actions_urgent'][0]}</li>
            <li>{TEXTS[st.session_state.language]['actions_urgent'][1]}</li>
            <li>{TEXTS[st.session_state.language]['actions_urgent'][2]}</li>
        </ul>
        <p style="color: {COLORS['success']}; font-weight: 600;">{t('roi')}</p>
    </div>
    """, unsafe_allow_html=True)

with col_rec2:
    st.markdown(f"""
    <div class="alert-card success">
        <h4 style="color: {COLORS['success']};">{t('opportunity')}</h4>
        <p><strong>{t('northeast_expansion')}</strong></p>
        <ul style="color: {COLORS['text_secondary']};">
            <li>{TEXTS[st.session_state.language]['actions_opportunity'][0]}</li>
            <li>{TEXTS[st.session_state.language]['actions_opportunity'][1]}</li>
            <li>{TEXTS[st.session_state.language]['actions_opportunity'][2]}</li>
        </ul>
        <p style="color: {COLORS['success']}; font-weight: 600;">{t('potential_customers')}</p>
    </div>
    """, unsafe_allow_html=True)

with col_rec3:
    st.markdown(f"""
    <div class="alert-card info">
        <h4 style="color: {COLORS['info']};">{t('optimization')}</h4>
        <p><strong>{t('last_mile')}</strong></p>
        <ul style="color: {COLORS['text_secondary']};">
            <li>{TEXTS[st.session_state.language]['actions_optimization'][0]}</li>
            <li>{TEXTS[st.session_state.language]['actions_optimization'][1]}</li>
            <li>{TEXTS[st.session_state.language]['actions_optimization'][2]}</li>
        </ul>
        <p style="color: {COLORS['success']}; font-weight: 600;">{t('cost_savings')}</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; padding: 2rem 0;">
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;">
        <span class="badge badge-info">Python</span>
        <span class="badge badge-info">SQL</span>
        <span class="badge badge-info">Streamlit</span>
        <span class="badge badge-info">Plotly</span>
        <span class="badge badge-success">Bilingual</span>
    </div>
    <p style="color: {COLORS['text_secondary']};">
        <strong>Brasil E-commerce Analytics</strong> · {t('developed_by')} DiSito 🤖<br>
        {t('dataset')} · 96K clientes · {t('tools')}<br>
        {datetime.now().strftime('%Y')} · {t('rights')}
    </p>
</div>
""", unsafe_allow_html=True)