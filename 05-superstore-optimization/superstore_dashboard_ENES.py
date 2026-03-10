import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="SuperStore · Profit Optimizer",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ESTADO DE TEMA E IDIOMA
# ============================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

if 'language' not in st.session_state:
    st.session_state.language = 'en'

# ============================================
# DICCIONARIO DE TEXTOS BILINGÜE
# ============================================
TEXTS = {
    'en': {
        # Header
        'title': 'SuperStore Profit Optimizer',
        'subtitle': 'Global Retail Analytics · Decision Intelligence',
        'period': 'Analyzed period',
        
        # Metrics
        'total_sales': '💰 TOTAL SALES',
        'net_profit': '📈 NET PROFIT',
        'margin': 'margin',
        'losses': '🚨 LOSSES',
        'markets': '🌍 MARKETS',
        'gross_revenue': 'Gross revenue',
        'negative_profit': 'Products with negative profit',
        'active_regions': 'Active regions',
        
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
        'categories': '#### 📦 Categories',
        'select_category': 'Select category',
        'all_categories': 'All',
        'threshold': '#### 💰 Profit threshold',
        'show_products': 'Show products with profit >',
        'generate_report': '📥 Generate Report',
        'generating': 'Generating report...',
        'report_ready': 'Report generated! (Demo)',
        'updated': '● Data updated',
        'records': '● Records',
        'last_update': 'Last update:',
        'disito_mode': '🎨 DiSito Mode',
        'classic_mode': '🌙 Classic Mode',
        
        # Alert
        'critical': 'CRITICAL',
        'discount_alert': 'Discounts >20% generate LOSSES',
        'estimated_impact': 'Estimated impact',
        'margin_alert': 'Margin >20%',
        'immediate_action': 'IMMEDIATE ACTION',
        'max_discount': 'Maximum discount limit to',
        'quick_stats': '📊 Quick Stats',
        'no_discount': 'No discount',
        'discount_1_20': '1-20%',
        'discount_20plus': '>20%',
        
        # Tabs
        'tab_discounts': '💸 Discounts',
        'tab_critical': '🩸 Critical Products',
        'tab_categories': '📦 Categories',
        'tab_logistics': '🚚 Logistics',
        'tab_regions': '🌍 Regions',
        'tab_actions': '🎯 Actions',
        
        # Discounts tab
        'discount_analysis': 'Discount Analysis',
        'avg_profit_by_range': 'Average Profit by Discount Range',
        'avg_profit': 'Average Profit ($)',
        'safe_zone': '✅ Safe Zone (0-20%)',
        'avg_profit_value': 'avg profit',
        'risk_zone': '⚠️ Risk Zone (21-30%)',
        'negative_margin': 'negative margin',
        'critical_zone': '💀 Critical Zone (>30%)',
        'net_loss': 'net loss',
        'no_data': 'No discount data available',
        
        # Critical products tab
        'products_with_losses': 'Products with Losses',
        'top_10_losses': 'Top 10 Products with Highest Losses',
        'loss': 'Loss ($)',
        'product': 'Product',
        'critical_details': '### 📋 Critical Products Detail',
        'total_loss': 'Total Loss',
        'negative_profit_impact': 'Negative impact on profit',
        'no_critical': '✅ No critical products identified',
        
        # Categories tab
        'profitability_by_category': 'Profitability by Category',
        'category': 'Category',
        'subcategory': 'Subcategory',
        'total_sales': 'Total Sales',
        'total_profit': 'Total Profit',
        'margin_percent': 'Margin %',
        'top_5_profitable': '### 🏆 Top 5 Profitable',
        'bottom_5': '### 💀 Bottom 5',
        'profit': 'Profit',
        'margin': 'Margin',
        'size': 'size',
        'color': 'color',
        'incomplete_data': 'Incomplete category data',
        
        # Logistics tab
        'logistics_efficiency': 'Logistics Efficiency',
        'shipping_cost_vs_profit': 'Shipping Cost vs Profit by Method',
        'shipping_cost': 'Shipping Cost',
        'profit_by_method': 'Profit by Method',
        'avg_cost': 'Average Cost',
        'total_profit_method': 'Total Profit',
        'method': 'Method',
        'no_logistics': 'No logistics data available',
        
        # Regions tab
        'regional_performance': 'Regional Performance',
        'profit_distribution': 'Profit Distribution by Market and Region',
        'unique_customers': 'Unique Customers',
        'top_5_regions': '### 🥇 Top 5 Regions',
        'bottom_5_regions': '### 📉 Bottom 5',
        'region': 'Region',
        'market': 'Market',
        'profit_region': 'Profit',
        'customers': 'Customers',
        'no_regional': 'No regional data available',
        
        # Actions tab
        'disito_action_plan': 'DiSito Action Plan',
        'profit_optimizer': 'Profit Optimizer',
        'urgent': '🚨 URGENT',
        'this_week': 'This Week',
        'actions_urgent': ['Limit discounts to 15%', 'Discontinue top 5 loss products', 'Audit pricing'],
        'impact_urgent': 'Impact: +$150K',
        'short_term': '⚠️ SHORT TERM',
        'this_month': 'This Month',
        'actions_short': ['Renegotiate shipping rates', 'Expand profitable categories', 'Reduce slow inventory'],
        'impact_short': 'Impact: +20% efficiency',
        'medium_term': '🎯 MEDIUM TERM',
        'this_quarter': 'This Quarter',
        'actions_medium': ['Focus on top margin regions', 'Exit unprofitable markets', 'Loyalty program'],
        'impact_medium': 'Impact: +25% profit',
        
        # Footer
        'developed_by': 'Crafted by José Granado with',
        'tools': 'Tools: SQL + Python + Streamlit',
        'rights': 'All profits deserve optimization',
        'style': 'DiSito Style',
        
        # Tooltips
        'tooltip_sales': 'Gross revenue for the period',
        'tooltip_profit': 'Net profit after discounts and costs',
        'tooltip_losses': 'Products with negative profit',
        'tooltip_markets': 'Active regions',
        'tooltip_date_range': 'Filter data by date',
        'tooltip_category': 'Filter by specific category',
    },
    'es': {
        # Header
        'title': 'SuperStore Optimizador de Ganancias',
        'subtitle': 'Analítica Global de Retail · Inteligencia de Decisiones',
        'period': 'Período analizado',
        
        # Metrics
        'total_sales': '💰 VENTAS TOTALES',
        'net_profit': '📈 GANANCIA NETA',
        'margin': 'margen',
        'losses': '🚨 PÉRDIDAS',
        'markets': '🌍 MERCADOS',
        'gross_revenue': 'Ingreso bruto del período',
        'negative_profit': 'Productos con ganancia negativa',
        'active_regions': 'Regiones activas',
        
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
        'categories': '#### 📦 Categorías',
        'select_category': 'Seleccionar categoría',
        'all_categories': 'Todas',
        'threshold': '#### 💰 Umbral de ganancia',
        'show_products': 'Mostrar productos con ganancia >',
        'generate_report': '📥 Generar Reporte',
        'generating': 'Generando reporte...',
        'report_ready': '¡Reporte generado! (Demo)',
        'updated': '● Datos actualizados',
        'records': '● Registros',
        'last_update': 'Última actualización:',
        'disito_mode': '🎨 Modo DiSito',
        'classic_mode': '🌙 Modo Clásico',
        
        # Alert
        'critical': 'CRÍTICO',
        'discount_alert': 'Descuentos >20% generan PÉRDIDAS',
        'estimated_impact': 'Impacto estimado',
        'margin_alert': 'Margen >20%',
        'immediate_action': 'ACCIÓN INMEDIATA',
        'max_discount': 'Límite máximo de descuento al',
        'quick_stats': '📊 Estadísticas Rápidas',
        'no_discount': 'Sin descuento',
        'discount_1_20': '1-20%',
        'discount_20plus': '>20%',
        
        # Tabs
        'tab_discounts': '💸 Descuentos',
        'tab_critical': '🩸 Productos Críticos',
        'tab_categories': '📦 Categorías',
        'tab_logistics': '🚚 Logística',
        'tab_regions': '🌍 Regiones',
        'tab_actions': '🎯 Acciones',
        
        # Discounts tab
        'discount_analysis': 'Análisis de Descuentos',
        'avg_profit_by_range': 'Ganancia Promedio por Rango de Descuento',
        'avg_profit': 'Ganancia Promedio ($)',
        'safe_zone': '✅ Zona Segura (0-20%)',
        'avg_profit_value': 'ganancia promedio',
        'risk_zone': '⚠️ Zona Riesgo (21-30%)',
        'negative_margin': 'margen negativo',
        'critical_zone': '💀 Zona Crítica (>30%)',
        'net_loss': 'pérdida neta',
        'no_data': 'No hay datos de descuentos',
        
        # Critical products tab
        'products_with_losses': 'Productos con Pérdidas',
        'top_10_losses': 'Top 10 Productos con Mayores Pérdidas',
        'loss': 'Pérdida ($)',
        'product': 'Producto',
        'critical_details': '### 📋 Detalle de Productos Críticos',
        'total_loss': 'Pérdida Total',
        'negative_profit_impact': 'Impacto negativo en ganancia',
        'no_critical': '✅ No hay productos críticos identificados',
        
        # Categories tab
        'profitability_by_category': 'Rentabilidad por Categoría',
        'category': 'Categoría',
        'subcategory': 'Subcategoría',
        'total_sales': 'Ventas Totales',
        'total_profit': 'Ganancia Total',
        'margin_percent': 'Margen %',
        'top_5_profitable': '### 🏆 Top 5 Rentables',
        'bottom_5': '### 💀 Bottom 5',
        'profit': 'Ganancia',
        'margin': 'Margen',
        'size': 'tamaño',
        'color': 'color',
        'incomplete_data': 'Datos de categorías incompletos',
        
        # Logistics tab
        'logistics_efficiency': 'Eficiencia Logística',
        'shipping_cost_vs_profit': 'Costo de Envío vs Ganancia por Método',
        'shipping_cost': 'Costo de Envío',
        'profit_by_method': 'Ganancia por Método',
        'avg_cost': 'Costo Promedio',
        'total_profit_method': 'Ganancia Total',
        'method': 'Método',
        'no_logistics': 'No hay datos logísticos',
        
        # Regions tab
        'regional_performance': 'Performance Regional',
        'profit_distribution': 'Distribución de Ganancia por Mercado y Región',
        'unique_customers': 'Clientes Únicos',
        'top_5_regions': '### 🥇 Top 5 Regiones',
        'bottom_5_regions': '### 📉 Bottom 5',
        'region': 'Región',
        'market': 'Mercado',
        'profit_region': 'Ganancia',
        'customers': 'Clientes',
        'no_regional': 'No hay datos regionales',
        
        # Actions tab
        'disito_action_plan': 'Plan de Acción DiSito',
        'profit_optimizer': 'Optimizador de Ganancias',
        'urgent': '🚨 URGENTE',
        'this_week': 'Esta Semana',
        'actions_urgent': ['Limitar descuentos a 15%', 'Descontinuar top 5 productos pérdida', 'Auditar pricing'],
        'impact_urgent': 'Impacto: +$150K',
        'short_term': '⚠️ CORTO PLAZO',
        'this_month': 'Este Mes',
        'actions_short': ['Renegociar tarifas envío', 'Expandir categorías rentables', 'Reducir inventario lento'],
        'impact_short': 'Impacto: +20% eficiencia',
        'medium_term': '🎯 MEDIANO PLAZO',
        'this_quarter': 'Este Trimestre',
        'actions_medium': ['Foco en regiones top margen', 'Salir de mercados no rentables', 'Programa fidelización'],
        'impact_medium': 'Impacto: +25% ganancia',
        
        # Footer
        'developed_by': 'Creado por José Granado con',
        'tools': 'Herramientas: SQL + Python + Streamlit',
        'rights': 'Todas las ganancias merecen optimización',
        'style': 'Estilo DiSito',
        
        # Tooltips
        'tooltip_sales': 'Ingreso bruto del período',
        'tooltip_profit': 'Ganancia neta después de descuentos y costos',
        'tooltip_losses': 'Productos con ganancia negativa',
        'tooltip_markets': 'Regiones activas',
        'tooltip_date_range': 'Filtra datos por fecha',
        'tooltip_category': 'Filtra por categoría específica',
    }
}

# Función helper para textos
def t(key):
    """Retorna texto en el idioma actual"""
    return TEXTS[st.session_state.language].get(key, key)

# ============================================
# PALETA DE COLORES DiSito
# ============================================
COLORS = {
    'primary': '#7C3AED',      # Morado vibrante
    'secondary': '#F59E0B',     # Naranja ámbar
    'success': '#10B981',        # Verde esmeralda
    'warning': '#EF4444',        # Rojo
    'info': '#3B82F6',           # Azul
    'purple_light': '#8B5CF6',   # Morado claro
    'purple_dark': '#6D28D9',    # Morado oscuro
    'background': '#0F172A' if st.session_state.theme == 'dark' else '#F8FAFC',
    'card_bg': '#1E293B' if st.session_state.theme == 'dark' else '#FFFFFF',
    'text': '#F1F5F9' if st.session_state.theme == 'dark' else '#0F172A',
    'text_secondary': '#94A3B8' if st.session_state.theme == 'dark' else '#475569',
    'border': '#334155' if st.session_state.theme == 'dark' else '#E2E8F0'
}

# ============================================
# CSS PROFESIONAL (con sidebar incluido)
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
    
    /* SIDEBAR - AHORA USA LOS COLORES DEL TEMA */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['card_bg']} !important;
        border-right: 1px solid {COLORS['border']} !important;
    }}
    
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {COLORS['text']} !important;
    }}
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] li, 
    section[data-testid="stSidebar"] span {{
        color: {COLORS['text']} !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['purple_dark']} 100%);
        color: white !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5);
    }}
    
    /* Tarjetas de métricas */
    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['card_bg']}dd 100%);
        padding: 1.5rem 1rem;
        border-radius: 20px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.1);
        transition: all 0.3s ease;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -10px rgba(124, 58, 237, 0.3);
        border-color: {COLORS['primary']};
    }}
    
    div[data-testid="stMetric"] label {{
        color: {COLORS['text_secondary']} !important;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {COLORS['primary']} !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}
    
    /* Botones */
    .stButton button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['purple_dark']} 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid {COLORS['border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {COLORS['text_secondary']} !important;
        font-weight: 500;
        transition: all 0.2s;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {COLORS['primary']} !important;
        border-bottom-color: {COLORS['primary']} !important;
        border-bottom-width: 3px;
    }}
    
    /* Badges */
    .badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    
    .badge-success {{
        background: rgba(16, 185, 129, 0.15);
        color: {COLORS['success']} !important;
        border: 1px solid {COLORS['success']}40;
    }}
    
    .badge-warning {{
        background: rgba(239, 68, 68, 0.15);
        color: {COLORS['warning']} !important;
        border: 1px solid {COLORS['warning']}40;
    }}
    
    .badge-info {{
        background: rgba(59, 130, 246, 0.15);
        color: {COLORS['info']} !important;
        border: 1px solid {COLORS['info']}40;
    }}
    
    /* Tarjetas de insight */
    .insight-card {{
        background: {COLORS['card_bg']};
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid {COLORS['border']};
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    
    /* Divider personalizado */
    .custom-divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, {COLORS['primary']} 50%, transparent 100%);
        margin: 2rem 0;
        opacity: 0.3;
    }}
    
    /* Headers con gradiente */
    .gradient-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['purple_light']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE CARGA
# ============================================
@st.cache_data(ttl=3600, show_spinner="🚀 Cargando datos...")
def load_superstore_data(db_path):
    """Carga todas las tablas"""
    
    tables = {
        'descuentos': "df_superstore_descuentos",
        'productos_criticos': "df_superstore_productos_criticos",
        'categorias': "df_superstore_categorias",
        'logistica': "df_superstore_logistica",
        'regiones': "df_superstore_regiones"
    }
    
    data = {}
    
    try:
        with sqlite3.connect(db_path) as conn:
            for key, table in tables.items():
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
                if cursor.fetchone():
                    df = pd.read_sql_query(f"SELECT * FROM [{table}]", conn)
                    df.columns = df.columns.str.strip().str.replace('"', '').str.lower()
                    data[key] = df
                else:
                    data[key] = pd.DataFrame()
        
        return data
        
    except Exception as e:
        st.error(f"💥 Error: {e}")
        return {}

# ============================================
# CARGA DE DATOS
# ============================================
DB_PATH = r"C:\Users\JOSE GRANADO PC\desktop\superstore-data\superstore.db"

with st.spinner("🎨 Preparando dashboard..."):
    data = load_superstore_data(DB_PATH)

if not data:
    st.error("❌ No hay datos. Revisá la ruta.")
    st.stop()

df_desc = data.get('descuentos', pd.DataFrame())
df_prod = data.get('productos_criticos', pd.DataFrame())
df_cat = data.get('categorias', pd.DataFrame())
df_log = data.get('logistica', pd.DataFrame())
df_reg = data.get('regiones', pd.DataFrame())

# ============================================
# SIDEBAR - FILTROS GLOBALES (AHORA CON COLORES CORRECTOS)
# ============================================

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: {COLORS['primary']};">🛒 SuperStore</h2>
        <p style="color: {COLORS['text_secondary']};">Profit Optimizer</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== SELECTOR DE IDIOMA =====
    st.markdown(f"<h4 style='color: {COLORS['text']} !important;'>{t('language')}</h4>", unsafe_allow_html=True)
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
    st.markdown(f"<h4 style='color: {COLORS['text']} !important;'>{t('theme')}</h4>", unsafe_allow_html=True)
    tema_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    tema_text = t('dark_mode') if st.session_state.theme == 'light' else t('light_mode')
    
    if st.button(f"{tema_icon} {tema_text}", use_container_width=True):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.rerun()
    
    st.markdown("---")
    
    st.markdown(f"<h4 style='color: {COLORS['text']} !important;'>{t('global_filters')}</h4>", unsafe_allow_html=True)
    
    # Métricas de resumen en sidebar
    st.markdown(f"""
    <div style="background: {COLORS['background']}; padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid {COLORS['border']};">
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem;">{t('transactions')}</p>
        <p style="margin: 0; font-size: 1.3rem; font-weight: 700; color: {COLORS['primary']};">1.7M</p>
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem; margin-top: 0.5rem;">{t('customers')}</p>
        <p style="margin: 0; font-size: 1.1rem; color: {COLORS['info']};">96K</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# HEADER PRINCIPAL
# ============================================
col_logo, col_title, col_toggle = st.columns([1, 3, 1])

with col_logo:
    st.markdown("""
    <div style="font-size: 3rem; text-align: center;">🛒</div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown(f"""
    <h1 style="margin: 0;">
        <span class="gradient-header">SuperStore</span> <span style="color: {COLORS['text']};">{t('title').replace('SuperStore ', '')}</span>
    </h1>
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
st.markdown(f"<h2>📊 <span class='gradient-header'>{t('total_sales')}</span></h2>", unsafe_allow_html=True)

total_ventas = df_cat['ventas_totales'].sum() if not df_cat.empty and 'ventas_totales' in df_cat.columns else 0
total_profit = df_cat['ganancia_total'].sum() if not df_cat.empty and 'ganancia_total' in df_cat.columns else 0
margen = (total_profit / total_ventas * 100) if total_ventas > 0 else 0
perdidas = abs(df_prod['perdida_total'].sum()) if not df_prod.empty and 'perdida_total' in df_prod.columns else 0
regiones = len(df_reg) if not df_reg.empty else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        t('total_sales'),
        f"${total_ventas:,.0f}",
        help=t('tooltip_sales')
    )

with col2:
    st.metric(
        t('net_profit'),
        f"${total_profit:,.0f}",
        delta=f"{margen:.1f}% {t('margin')}",
        delta_color="normal",
        help=t('tooltip_profit')
    )

with col3:
    st.metric(
        t('losses'),
        f"${perdidas:,.0f}",
        delta=f"-{(perdidas/total_profit*100):.1f}%" if total_profit > 0 else None,
        delta_color="inverse",
        help=t('tooltip_losses')
    )

with col4:
    st.metric(
        t('markets'),
        f"{regiones}",
        help=t('tooltip_markets')
    )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# ALERTA INTERACTIVA
# ============================================

col_alert, col_stats = st.columns([2, 1])

with col_alert:
    perdida_desc = 0
    if not df_desc.empty and 'nivel_descuento' in df_desc.columns and 'ganancia_promedio' in df_desc.columns:
        df_desc['descuento_pct'] = (df_desc['nivel_descuento'] * 100).round(0)
        perdida_desc = abs(df_desc[df_desc['descuento_pct'] > 20]['ganancia_promedio'].sum())
    
    st.markdown(f"""
    <div class="insight-card">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="font-size: 2rem;">🚨</span>
            <span class="badge badge-warning" style="font-size: 1rem;">{t('critical')}</span>
        </div>
        <h3 style="color: {COLORS['warning']};">{t('discount_alert')}</h3>
        <div style="display: flex; gap: 2rem; margin: 1.5rem 0;">
            <div>
                <p style="color: {COLORS['text_secondary']}; margin: 0;">{t('estimated_impact')}</p>
                <p style="font-size: 2rem; font-weight: 700; color: {COLORS['warning']}; margin: 0;">${perdida_desc:,.0f}</p>
            </div>
            <div>
                <p style="color: {COLORS['text_secondary']}; margin: 0;">{t('margin_alert')}</p>
                <p style="font-size: 2rem; font-weight: 700; color: {COLORS['warning']}; margin: 0;">-8.7%</p>
            </div>
        </div>
        <p style="background: {COLORS['warning']}20; padding: 1rem; border-radius: 12px;">
            <strong>{t('immediate_action')}:</strong> {t('max_discount')} <strong>15%</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_stats:
    st.markdown(f"""
    <div class="insight-card">
        <h4 style="color: {COLORS['primary']};">{t('quick_stats')}</h4>
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between;">
                <span>{t('no_discount')}</span>
                <span style="color: {COLORS['success']};">41% {t('margin')}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>{t('discount_1_20')}</span>
                <span style="color: {COLORS['secondary']};">16-30%</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>{t('discount_20plus')}</span>
                <span style="color: {COLORS['warning']};">-69% {t('margin')}</span>
            </div>
        </div>
        <div style="height: 4px; background: linear-gradient(90deg, {COLORS['success']} 0%, {COLORS['secondary']} 50%, {COLORS['warning']} 100%); border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TABS
# ============================================
tabs = st.tabs([
    t('tab_discounts'),
    t('tab_critical'),
    t('tab_categories'),
    t('tab_logistics'),
    t('tab_regions'),
    t('tab_actions')
])

# ============================================
# TAB 1: DESCUENTOS
# ============================================
with tabs[0]:
    st.markdown(f"<h3><span class='gradient-header'>{t('discount_analysis')}</span></h3>", unsafe_allow_html=True)
    
    if not df_desc.empty:
        df_desc_clean = df_desc.copy()
        df_desc_clean['descuento_pct'] = (df_desc_clean['nivel_descuento'] * 100).round(0)
        
        def cat_desc(pct):
            if pct == 0:
                return '0%'
            elif pct <= 10:
                return '1-10%'
            elif pct <= 20:
                return '11-20%'
            elif pct <= 30:
                return '21-30%'
            else:
                return '>30%'
        
        df_desc_clean['rango'] = df_desc_clean['descuento_pct'].apply(cat_desc)
        
        desc_group = df_desc_clean.groupby('rango').agg({
            'ganancia_promedio': 'mean',
            'nivel_descuento': 'count'
        }).reset_index()
        
        orden = ['0%', '1-10%', '11-20%', '21-30%', '>30%']
        desc_group['rango'] = pd.Categorical(desc_group['rango'], categories=orden, ordered=True)
        desc_group = desc_group.sort_values('rango')
        
        fig_desc = go.Figure()
        
        for i, row in desc_group.iterrows():
            color = COLORS['success'] if row['rango'] in ['0%', '1-10%', '11-20%'] else COLORS['warning']
            fig_desc.add_trace(go.Bar(
                x=[row['rango']],
                y=[row['ganancia_promedio']],
                name=row['rango'],
                marker_color=color,
                text=f"${row['ganancia_promedio']:.2f}",
                textposition='outside',
                showlegend=False
            ))
        
        fig_desc.add_hline(y=0, line_dash="dash", line_color=COLORS['text_secondary'])
        fig_desc.update_layout(
            title=t('avg_profit_by_range'),
            yaxis_title=t('avg_profit'),
            height=500,
            plot_bgcolor=COLORS['card_bg'],
            paper_bgcolor=COLORS['background']
        )
        
        st.plotly_chart(fig_desc, use_container_width=True)
        
        col_d1, col_d2, col_d3 = st.columns(3)
        
        with col_d1:
            safe_mean = desc_group[desc_group['rango'].isin(['0%', '1-10%', '11-20%'])]['ganancia_promedio'].mean()
            st.metric(
                t('safe_zone'),
                f"${safe_mean:.2f}",
                t('avg_profit_value')
            )
        
        with col_d2:
            if '21-30%' in desc_group['rango'].values:
                risk_val = desc_group[desc_group['rango']=='21-30%']['ganancia_promedio'].values[0]
                st.metric(
                    t('risk_zone'),
                    f"${risk_val:.2f}",
                    t('negative_margin'),
                    delta_color="inverse"
                )
        
        with col_d3:
            if '>30%' in desc_group['rango'].values:
                crit_val = desc_group[desc_group['rango']=='>30%']['ganancia_promedio'].values[0]
                st.metric(
                    t('critical_zone'),
                    f"${crit_val:.2f}",
                    t('net_loss'),
                    delta_color="inverse"
                )
    else:
        st.info(t('no_data'))

# ============================================
# TAB 2: PRODUCTOS CRÍTICOS
# ============================================
with tabs[1]:
    st.markdown(f"<h3><span class='gradient-header'>{t('products_with_losses')}</span></h3>", unsafe_allow_html=True)
    
    if not df_prod.empty:
        col_nombre = next((c for c in df_prod.columns if any(x in c for x in ['product', 'nombre'])), df_prod.columns[0])
        col_perdida = next((c for c in df_prod.columns if any(x in c for x in ['perdida', 'loss'])), None)
        
        if col_perdida:
            top_loss = df_prod.nsmallest(10, col_perdida)
            
            fig_loss = px.bar(
                top_loss,
                x=col_perdida,
                y=col_nombre,
                orientation='h',
                title=t('top_10_losses'),
                labels={col_perdida: t('loss'), col_nombre: ''},
                color=col_perdida,
                color_continuous_scale='Reds',
                text=col_perdida
            )
            
            fig_loss.update_traces(
                texttemplate='-$%{text:.0f}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig_loss.update_layout(
                height=600,
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['background']
            )
            
            st.plotly_chart(fig_loss, use_container_width=True)
            
            st.markdown(t('critical_details'))
            
            loss_display = df_prod[[col_nombre, col_perdida]].copy()
            loss_display[col_perdida] = loss_display[col_perdida].apply(lambda x: f"${x:,.2f}")
            loss_display.columns = [t('product'), t('total_loss')]
            
            st.dataframe(
                loss_display,
                hide_index=True,
                use_container_width=True,
                column_config={
                    t('product'): st.column_config.TextColumn(t('product')),
                    t('total_loss'): st.column_config.TextColumn(t('total_loss'), help=t('negative_profit_impact'))
                }
            )
    else:
        st.success(t('no_critical'))

# ============================================
# TAB 3: CATEGORÍAS
# ============================================
with tabs[2]:
    st.markdown(f"<h3><span class='gradient-header'>{t('profitability_by_category')}</span></h3>", unsafe_allow_html=True)
    
    if not df_cat.empty and all(c in df_cat.columns for c in ['category', 'sub_category', 'ventas_totales', 'ganancia_total']):
        
        df_cat['margen'] = (df_cat['ganancia_total'] / df_cat['ventas_totales'] * 100).fillna(0)
        
        fig_tree = px.treemap(
            df_cat,
            path=[px.Constant("SuperStore"), 'category', 'sub_category'],
            values='ventas_totales',
            color='margen',
            color_continuous_scale=['#EF4444', '#F59E0B', '#10B981', '#7C3AED'],
            title=f"{t('profitability_by_category')} ({t('total_sales')} = {t('size')}, {t('margin_percent')} = {t('color')})",
            hover_data={'ganancia_total': ':,.0f', 'margen': ':.1f'}
        )
        
        fig_tree.update_layout(
            height=600,
            plot_bgcolor=COLORS['card_bg'],
            paper_bgcolor=COLORS['background']
        )
        
        st.plotly_chart(fig_tree, use_container_width=True)
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown(t('top_5_profitable'))
            top_cat = df_cat.nlargest(5, 'ganancia_total')[['sub_category', 'ganancia_total', 'margen']]
            top_cat['ganancia_total'] = top_cat['ganancia_total'].apply(lambda x: f"${x:,.0f}")
            top_cat['margen'] = top_cat['margen'].apply(lambda x: f"{x:.1f}%")
            top_cat.columns = [t('subcategory'), t('profit'), t('margin')]
            st.dataframe(top_cat, hide_index=True, use_container_width=True)
        
        with col_t2:
            st.markdown(t('bottom_5'))
            bottom_cat = df_cat.nsmallest(5, 'ganancia_total')[['sub_category', 'ganancia_total', 'margen']]
            bottom_cat['ganancia_total'] = bottom_cat['ganancia_total'].apply(lambda x: f"${x:,.0f}")
            bottom_cat['margen'] = bottom_cat['margen'].apply(lambda x: f"{x:.1f}%")
            bottom_cat.columns = [t('subcategory'), t('profit'), t('margin')]
            st.dataframe(bottom_cat, hide_index=True, use_container_width=True)
    else:
        st.warning(t('incomplete_data'))

# ============================================
# TAB 4: LOGÍSTICA
# ============================================
with tabs[3]:
    st.markdown(f"<h3><span class='gradient-header'>{t('logistics_efficiency')}</span></h3>", unsafe_allow_html=True)
    
    if not df_log.empty:
        col_ship = next((c for c in df_log.columns if 'ship' in c or 'envio' in c), None)
        
        if col_ship and all(c in df_log.columns for c in ['costo_envio_promedio', 'ganancia_por_metodo']):
            
            fig_log = go.Figure()
            
            fig_log.add_trace(go.Bar(
                name=t('shipping_cost'),
                x=df_log[col_ship],
                y=df_log['costo_envio_promedio'],
                marker_color=COLORS['info'],
                text=df_log['costo_envio_promedio'].apply(lambda x: f'${x:.2f}'),
                textposition='outside'
            ))
            
            fig_log.add_trace(go.Scatter(
                name=t('profit_by_method'),
                x=df_log[col_ship],
                y=df_log['ganancia_por_metodo'],
                mode='lines+markers',
                marker_color=COLORS['success'],
                yaxis='y2',
                line=dict(width=3, color=COLORS['success']),
                marker=dict(size=10)
            ))
            
            fig_log.update_layout(
                title=t('shipping_cost_vs_profit'),
                yaxis=dict(title=t('avg_cost')),
                yaxis2=dict(title=t('total_profit_method'), overlaying='y', side='right'),
                height=500,
                hovermode='x unified',
                plot_bgcolor=COLORS['card_bg'],
                paper_bgcolor=COLORS['background']
            )
            
            st.plotly_chart(fig_log, use_container_width=True)
            
            st.markdown(f"### {t('method')}")
            log_display = df_log[[col_ship, 'costo_envio_promedio', 'ganancia_por_metodo']].copy()
            log_display.columns = [t('method'), t('avg_cost'), t('total_profit_method')]
            log_display[t('avg_cost')] = log_display[t('avg_cost')].apply(lambda x: f"${x:.2f}")
            log_display[t('total_profit_method')] = log_display[t('total_profit_method')].apply(lambda x: f"${x:,.0f}")
            
            st.dataframe(log_display, hide_index=True, use_container_width=True)
    else:
        st.info(t('no_logistics'))

# ============================================
# TAB 5: REGIONES
# ============================================
with tabs[4]:
    st.markdown(f"<h3><span class='gradient-header'>{t('regional_performance')}</span></h3>", unsafe_allow_html=True)
    
    if not df_reg.empty and all(c in df_reg.columns for c in ['market', 'region', 'ventas', 'ganancia']):
        
        fig_sun = px.sunburst(
            df_reg,
            path=['market', 'region'],
            values='ventas',
            color='ganancia',
            color_continuous_scale=['#EF4444', '#F59E0B', '#10B981', '#7C3AED'],
            title=t('profit_distribution'),
            hover_data={'clientes_unicos': True}
        )
        
        fig_sun.update_layout(
            height=600,
            plot_bgcolor=COLORS['card_bg'],
            paper_bgcolor=COLORS['background']
        )
        
        st.plotly_chart(fig_sun, use_container_width=True)
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.markdown(t('top_5_regions'))
            top_reg = df_reg.nlargest(5, 'ganancia')[['region', 'market', 'ganancia', 'clientes_unicos']]
            top_reg['ganancia'] = top_reg['ganancia'].apply(lambda x: f"${x:,.0f}")
            top_reg.columns = [t('region'), t('market'), t('profit_region'), t('customers')]
            st.dataframe(top_reg, hide_index=True, use_container_width=True)
        
        with col_r2:
            st.markdown(t('bottom_5_regions'))
            bottom_reg = df_reg.nsmallest(5, 'ganancia')[['region', 'market', 'ganancia', 'clientes_unicos']]
            bottom_reg['ganancia'] = bottom_reg['ganancia'].apply(lambda x: f"${x:,.0f}")
            bottom_reg.columns = [t('region'), t('market'), t('profit_region'), t('customers')]
            st.dataframe(bottom_reg, hide_index=True, use_container_width=True)
    else:
        st.info(t('no_regional'))

# ============================================
# TAB 6: ACCIONES
# ============================================
with tabs[5]:
    st.markdown(f"<h3><span class='gradient-header'>{t('disito_action_plan')}</span></h3>", unsafe_allow_html=True)
    
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        st.markdown(f"""
        <div class="insight-card">
            <span class="badge badge-warning" style="font-size: 1rem;">{t('urgent')}</span>
            <h4 style="color: {COLORS['warning']};">{t('this_week')}</h4>
            <ul style="color: {COLORS['text_secondary']};">
                <li>{TEXTS[st.session_state.language]['actions_urgent'][0]}</li>
                <li>{TEXTS[st.session_state.language]['actions_urgent'][1]}</li>
                <li>{TEXTS[st.session_state.language]['actions_urgent'][2]}</li>
            </ul>
            <p style="color: {COLORS['success']}; font-weight: 600;">{t('impact_urgent')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_a2:
        st.markdown(f"""
        <div class="insight-card">
            <span class="badge badge-info" style="font-size: 1rem;">{t('short_term')}</span>
            <h4 style="color: {COLORS['info']};">{t('this_month')}</h4>
            <ul style="color: {COLORS['text_secondary']};">
                <li>{TEXTS[st.session_state.language]['actions_short'][0]}</li>
                <li>{TEXTS[st.session_state.language]['actions_short'][1]}</li>
                <li>{TEXTS[st.session_state.language]['actions_short'][2]}</li>
            </ul>
            <p style="color: {COLORS['success']}; font-weight: 600;">{t('impact_short')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_a3:
        st.markdown(f"""
        <div class="insight-card">
            <span class="badge badge-success" style="font-size: 1rem;">{t('medium_term')}</span>
            <h4 style="color: {COLORS['success']};">{t('this_quarter')}</h4>
            <ul style="color: {COLORS['text_secondary']};">
                <li>{TEXTS[st.session_state.language]['actions_medium'][0]}</li>
                <li>{TEXTS[st.session_state.language]['actions_medium'][1]}</li>
                <li>{TEXTS[st.session_state.language]['actions_medium'][2]}</li>
            </ul>
            <p style="color: {COLORS['success']}; font-weight: 600;">{t('impact_medium')}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; padding: 2rem;">
    <div style="display: flex; justify-content: center; gap: 0.5rem; margin-bottom: 1rem;">
        <span class="badge badge-info">Python</span>
        <span class="badge badge-info">SQL</span>
        <span class="badge badge-info">Streamlit</span>
        <span class="badge badge-info">Plotly</span>
        <span class="badge badge-success">{t('style')}</span>
        <span class="badge badge-success">Bilingual</span>
    </div>
    <p style="color: {COLORS['text_secondary']};">SuperStore {t('profit_optimizer')} · {t('developed_by')} 🎨 DiSito</p>
    <p style="color: {COLORS['text_secondary']};">{datetime.now().strftime('%Y')} · {t('rights')}</p>
</div>
""", unsafe_allow_html=True)