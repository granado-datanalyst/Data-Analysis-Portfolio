import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CONFIGURACIÓN DE PÁGINA Y ESTILO
# ============================================
st.set_page_config(
    page_title="Retail UK · Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONFIGURACIÓN DE ESTADO (TEMA E IDIOMA)
# ============================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # 'dark' or 'light'

if 'language' not in st.session_state:
    st.session_state.language = 'en'  # 'en' or 'es'

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
    'gradient_start': '#8B5CF6' if st.session_state.theme == 'dark' else '#2E4057',
    'gradient_end': '#A78BFA' if st.session_state.theme == 'dark' else '#048BA8'
}

# ============================================
# DICCIONARIO DE TEXTOS BILINGÜE
# ============================================
TEXTS = {
    'en': {
        # Header
        'title': '🇬🇧 Retail UK · Performance Dashboard',
        'subtitle': 'Complete analysis of 1.7M transactions | Online Retail Dataset',
        'period': 'Analyzed period',
        
        # Metrics
        'revenue_risk': '💰 Revenue at Risk',
        'vip_customers': '💎 VIP Customers',
        'main_market': '🌍 Main Market',
        'problem_products': '🚨 Problem Products',
        'avg_ticket': '📊 Average Ticket',
        'of_total': 'of total',
        
        # Sidebar
        'global_filters': '🔍 Global Filters',
        'transactions': '📦 Transactions',
        'customers': '👥 Customers',
        'period_filter': '#### 📅 Period',
        'date_range': 'Date range',
        'countries': '#### 🌍 Countries',
        'select_country': 'Select country',
        'all_countries': 'All',
        'sales_threshold': '#### 💰 Sales threshold',
        'show_products': 'Show products with sales >',
        'generate_pdf': '📥 Generate PDF Report',
        'generating': 'Generating report...',
        'report_ready': 'Report generated! (Demo)',
        'updated': '● Data updated',
        'records': '● 1.7M records',
        'last_update': 'Last update:',
        'theme_toggle': 'Theme',
        'dark_mode': '🌙 Dark Mode',
        'light_mode': '☀️ Light Mode',
        
        # Tabs
        'tab_overview': '📊 Overview',
        'tab_products': '🏷️ Products Analysis',
        'tab_customers': '👥 Customer Segmentation',
        'tab_geography': '🌍 Geography',
        'tab_insights': '💡 Insights & Actions',
        
        # Overview tab
        'kpi_trends': '### 📈 KPIs and Trends',
        'top_products': '🏆 Top 10 Products by Revenue',
        'performance_dist': 'Performance Distribution by Country',
        'view_full_table': '📋 View full product table',
        'product': 'Product',
        'total_revenue': 'Total Revenue',
        'units_sold': 'Units Sold',
        
        # Products tab
        'detailed_analysis': '### 🏷️ Detailed Product Analysis',
        'problematic_products': '🚨 Problematic Products',
        'uncategorized_revenue': 'in uncategorized revenue',
        'top_10_problematic': 'Top 10 Problematic Products',
        'top_performers': '✅ Top Performers',
        'high_performance': 'high performance products',
        'top_10_revenue': 'Top 10 Products by Revenue',
        'performance_comparison': '### 📊 Performance Comparison',
        'avg_top_products': 'Avg Top Products',
        'avg_problematic': 'Avg Problematic',
        'efficiency_ratio': 'Efficiency Ratio',
        
        # Customers tab
        'customer_analysis': '### 👥 Customer Analysis',
        'category_distribution': 'Distribution by Category',
        'value_by_category': 'Total Value by Category',
        'top_10_vip': '### 💎 Top 10 VIP Customers',
        'no_vip': 'No VIP customers in dataset',
        
        # Geography tab
        'geo_analysis': '### 🌍 Geographic Analysis',
        'top_20_countries': 'Top 20 Countries by Sales',
        'concentration': '📊 Concentration',
        'in_top_3': 'in top 3 countries',
        'performance_by': '#### 🎯 Distribution by performance',
        'excellent': '🔥 Excellent',
        'good': '👍 Good',
        'poor': '⚠️ Poor',
        'countries': 'countries',
        'top_5_ticket': '#### 💳 Top 5 Average Ticket',
        
        # Insights tab
        'strategic_insights': '### 💡 Strategic Insights',
        'critical_risk': '⚠️ CRITICAL RISK',
        'uncategorized_revenue_short': 'Uncategorized revenue',
        'immediate_action': '🎯 IMMEDIATE ACTION',
        'vip_opportunity': '✅ VIP OPPORTUNITY',
        'high_value_customers': 'High value customers',
        'retention_program': '🎯 RETENTION PROGRAM',
        'expansion': '🌍 EXPANSION',
        'concentration_top3': 'Concentration in top 3 countries',
        'diversification': '🎯 DIVERSIFICATION STRATEGY',
        'recommended_plan': '### 📋 Recommended Action Plan',
        
        # Action items
        'high_priority': 'HIGH',
        'medium_priority': 'MEDIUM',
        'low_priority': 'LOW',
        'action_catalog': 'Urgent catalog audit',
        'action_naming': 'Standardize product naming',
        'action_validation': 'Implement data validation',
        'action_discounts': 'Exclusive discounts',
        'action_early_access': 'Early access to new products',
        'action_support': 'Priority support',
        'action_secondary': 'Analyze secondary markets',
        'action_campaigns': 'Localized campaigns',
        'action_logistics': 'Optimize international logistics',
        'action_automation': 'Automate reports and alerts',
        
        # Impacts
        'impact_recoverable': '£150K recoverable',
        'impact_retention': '+20% retention',
        'impact_new_revenue': '+15% new revenue',
        'impact_efficiency': 'Operational efficiency',
        
        # Footer
        'developed_by': 'Developed by José Granado',
        'dataset': 'Dataset: Online Retail II',
        'tools': 'Tools: SQL + Python + Streamlit',
        'rights': 'All rights reserved',
        
        # Tooltips
        'tooltip_revenue_risk': 'Products with problematic names ("garbage" descriptions)',
        'tooltip_vip': 'Customers who spent >£5,000',
        'tooltip_main_market': 'Country with highest sales',
        'tooltip_problem_products': 'Products with inconsistent descriptions',
        'tooltip_avg_ticket': 'Global average per invoice',
        'tooltip_date_range': 'Filter data by invoice date',
        'tooltip_country': 'Filter analysis by specific country',
    },
    'es': {
        # Header
        'title': '🇬🇧 Retail UK · Dashboard de Performance',
        'subtitle': 'Análisis completo de 1.7M transacciones | Online Retail Dataset',
        'period': 'Período analizado',
        
        # Metrics
        'revenue_risk': '💰 Ingresos en Riesgo',
        'vip_customers': '💎 Clientes VIP',
        'main_market': '🌍 Mercado Principal',
        'problem_products': '🚨 Productos Problema',
        'avg_ticket': '📊 Ticket Promedio',
        'of_total': 'del total',
        
        # Sidebar
        'global_filters': '🔍 Filtros Globales',
        'transactions': '📦 Transacciones',
        'customers': '👥 Clientes',
        'period_filter': '#### 📅 Período',
        'date_range': 'Rango de fechas',
        'countries': '#### 🌍 Países',
        'select_country': 'Seleccionar país',
        'all_countries': 'Todos',
        'sales_threshold': '#### 💰 Umbral de ventas',
        'show_products': 'Mostrar productos con ventas >',
        'generate_pdf': '📥 Generar Reporte PDF',
        'generating': 'Generando reporte...',
        'report_ready': '¡Reporte generado! (Demo)',
        'updated': '● Datos actualizados',
        'records': '● 1.7M registros',
        'last_update': 'Última actualización:',
        'theme_toggle': 'Tema',
        'dark_mode': '🌙 Modo Oscuro',
        'light_mode': '☀️ Modo Claro',
        
        # Tabs
        'tab_overview': '📊 Visión General',
        'tab_products': '🏷️ Análisis de Productos',
        'tab_customers': '👥 Segmentación Clientes',
        'tab_geography': '🌍 Geografía',
        'tab_insights': '💡 Insights & Acciones',
        
        # Overview tab
        'kpi_trends': '### 📈 KPIs y Tendencias',
        'top_products': '🏆 Top 10 Productos por Ingresos',
        'performance_dist': 'Distribución de Rendimiento por País',
        'view_full_table': '📋 Ver tabla completa de productos',
        'product': 'Producto',
        'total_revenue': 'Ingresos Totales',
        'units_sold': 'Unidades Vendidas',
        
        # Products tab
        'detailed_analysis': '### 🏷️ Análisis Detallado de Productos',
        'problematic_products': '🚨 Productos Problemáticos',
        'uncategorized_revenue': 'en ingresos no categorizados',
        'top_10_problematic': 'Top 10 Productos Problemáticos',
        'top_performers': '✅ Top Performers',
        'high_performance': 'productos de alto rendimiento',
        'top_10_revenue': 'Top 10 Productos por Ingresos',
        'performance_comparison': '### 📊 Comparativa de Performance',
        'avg_top_products': 'Promedio Top Productos',
        'avg_problematic': 'Promedio Problemáticos',
        'efficiency_ratio': 'Ratio de eficiencia',
        
        # Customers tab
        'customer_analysis': '### 👥 Análisis de Clientes',
        'category_distribution': 'Distribución por Categoría',
        'value_by_category': 'Valor Total por Categoría',
        'top_10_vip': '### 💎 Top 10 Clientes VIP',
        'no_vip': 'No hay clientes VIP en el dataset',
        
        # Geography tab
        'geo_analysis': '### 🌍 Análisis Geográfico',
        'top_20_countries': 'Top 20 Países por Ventas',
        'concentration': '📊 Concentración',
        'in_top_3': 'en top 3 países',
        'performance_by': '#### 🎯 Distribución por rendimiento',
        'excellent': '🔥 Excelente',
        'good': '👍 Bueno',
        'poor': '⚠️ Bajo',
        'countries': 'países',
        'top_5_ticket': '#### 💳 Top 5 Ticket Promedio',
        
        # Insights tab
        'strategic_insights': '### 💡 Insights Estratégicos',
        'critical_risk': '⚠️ RIESGO CRÍTICO',
        'uncategorized_revenue_short': 'Ingresos no categorizados',
        'immediate_action': '🎯 ACCIÓN INMEDIATA',
        'vip_opportunity': '✅ OPORTUNIDAD VIP',
        'high_value_customers': 'Clientes de alto valor',
        'retention_program': '🎯 PROGRAMA DE RETENCIÓN',
        'expansion': '🌍 EXPANSIÓN',
        'concentration_top3': 'Concentración en top 3 países',
        'diversification': '🎯 ESTRATEGIA DE DIVERSIFICACIÓN',
        'recommended_plan': '### 📋 Plan de Acción Recomendado',
        
        # Action items
        'high_priority': 'ALTA',
        'medium_priority': 'MEDIA',
        'low_priority': 'BAJA',
        'action_catalog': 'Auditoría de catálogo urgente',
        'action_naming': 'Estandarizar naming de productos',
        'action_validation': 'Implementar validaciones en carga',
        'action_discounts': 'Descuentos exclusivos',
        'action_early_access': 'Acceso anticipado a novedades',
        'action_support': 'Soporte prioritario',
        'action_secondary': 'Analizar mercados secundarios',
        'action_campaigns': 'Campañas localizadas',
        'action_logistics': 'Optimizar logística internacional',
        'action_automation': 'Automatizar reportes y alertas',
        
        # Impacts
        'impact_recoverable': '£150K recuperables',
        'impact_retention': '+20% retención',
        'impact_new_revenue': '+15% nuevos ingresos',
        'impact_efficiency': 'Eficiencia operativa',
        
        # Footer
        'developed_by': 'Desarrollado por José Granado',
        'dataset': 'Dataset: Online Retail II',
        'tools': 'Herramientas: SQL + Python + Streamlit',
        'rights': 'Todos los derechos reservados',
        
        # Tooltips
        'tooltip_revenue_risk': 'Productos con nombres problemáticos (descripciones "basura")',
        'tooltip_vip': 'Clientes que gastaron >£5,000',
        'tooltip_main_market': 'País con mayores ventas',
        'tooltip_problem_products': 'Productos con descripciones inconsistentes',
        'tooltip_avg_ticket': 'Promedio global por factura',
        'tooltip_date_range': 'Filtra los datos por fecha de factura',
        'tooltip_country': 'Filtra el análisis por país específico',
    }
}

# Función helper para textos
def t(key):
    """Retorna texto en el idioma actual"""
    return TEXTS[st.session_state.language].get(key, key)

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
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: {COLORS['primary']};
    }}
    
    div[data-testid="stMetric"] label {{
        color: {COLORS['text_secondary']} !important;
        font-weight: 500 !important;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {COLORS['primary']} !important;
        font-weight: 700;
        font-size: 1.8rem;
    }}
    
    .stButton button {{
        background-color: {COLORS['secondary']};
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(241, 143, 1, 0.3);
    }}
    
    .stButton button:hover {{
        background-color: #d47d00;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(241, 143, 1, 0.4);
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
    
    .streamlit-expanderHeader {{
        background-color: {COLORS['card_bg']};
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
        font-weight: 500;
    }}
    
    .dataframe {{
        font-family: 'Inter', sans-serif;
        border: none !important;
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['card_bg']};
        border-right: 1px solid {COLORS['border']};
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
    }}
    
    .badge-warning {{
        background-color: rgba(239, 68, 68, 0.1);
        color: {COLORS['warning']} !important;
    }}
    
    .badge-info {{
        background-color: rgba(59, 130, 246, 0.1);
        color: {COLORS['info']} !important;
    }}
    
    .insight-card {{
        background-color: {COLORS['card_bg']};
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 4px solid;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }}
    
    .insight-card.warning {{
        border-left-color: {COLORS['warning']};
    }}
    
    .insight-card.success {{
        border-left-color: {COLORS['success']};
    }}
    
    .insight-card.info {{
        border-left-color: {COLORS['info']};
    }}
    
    .custom-divider {{
        height: 2px;
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['info']} 50%, transparent 100%);
        margin: 2rem 0;
        opacity: 0.2;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE CARGA DE DATOS
# ============================================

@st.cache_data(ttl=3600, show_spinner="Cargando datos desde la base...")
def load_table_from_sql(table_name):
    """Carga una tabla desde SQLite con manejo seguro de conexiones."""
    if not table_name.replace('_', '').replace('df', '').isalnum():
        st.error(f"Nombre de tabla inválido: {table_name}")
        return pd.DataFrame()
    
    DB_PATH = r"C:\Users\JOSE GRANADO PC\desktop\retail-data\retail.db"
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not cursor.fetchone():
                st.error(f"La tabla '{table_name}' no existe en la base de datos")
                return pd.DataFrame()
            
            df = pd.read_sql_query(f"SELECT * FROM [{table_name}]", conn)
            
            date_columns = [col for col in df.columns if 'date' in col.lower() or 'fecha' in col.lower()]
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
            
            return df
            
    except sqlite3.Error as e:
        st.error(f"Error de base de datos: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error inesperado cargando {table_name}: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_metadata():
    """Obtiene metadatos de la base de datos"""
    DB_PATH = r"C:\Users\JOSE GRANADO PC\desktop\retail-data\retail.db"
    
    with sqlite3.connect(DB_PATH) as conn:
        total_transacciones = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM online_retail_II", 
            conn
        ).iloc[0]['count']
        
        fecha_range = pd.read_sql_query(
            "SELECT MIN(InvoiceDate) as min_date, MAX(InvoiceDate) as max_date FROM online_retail_II",
            conn
        ).iloc[0]
        
        total_clientes = pd.read_sql_query(
            "SELECT COUNT(DISTINCT `Customer ID`) as count FROM online_retail_II WHERE `Customer ID` IS NOT NULL",
            conn
        ).iloc[0]['count']
        
        return {
            'total_transacciones': total_transacciones,
            'fecha_min': pd.to_datetime(fecha_range['min_date']),
            'fecha_max': pd.to_datetime(fecha_range['max_date']),
            'total_clientes': total_clientes
        }

@st.cache_data(ttl=3600)
def load_all_data():
    """Carga todos los datasets necesarios"""
    
    tables = [
        "df_productos_problematicos",
        "df_segmentacion_clientes", 
        "df_performance_regiones",
        "df_top_productos",
        "df_ticket_promedio_paises"
    ]
    
    data = {}
    for table in tables:
        data[table] = load_table_from_sql(table)
        if data[table].empty:
            st.warning(f"No se pudo cargar la tabla: {table}")
    
    return data

# Cargar datos y metadata
with st.spinner('🔄 Conectando a la base de datos...'):
    data = load_all_data()
    metadata = get_metadata()

if not data:
    st.error("❌ No se pudo cargar ningún dato. Verifica la conexión a la base.")
    st.stop()

# Asignar a variables
df_problemas = data.get("df_productos_problematicos", pd.DataFrame())
df_clientes = data.get("df_segmentacion_clientes", pd.DataFrame())
df_regiones = data.get("df_performance_regiones", pd.DataFrame())
df_top_productos = data.get("df_top_productos", pd.DataFrame())
df_ticket = data.get("df_ticket_promedio_paises", pd.DataFrame())

# ============================================
# SIDEBAR - FILTROS GLOBALES
# ============================================

with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: {COLORS['primary']}; margin: 0;">📊 Retail UK</h2>
        <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== SELECTOR DE IDIOMA =====
    st.markdown(f"### 🌐 Language / Idioma")
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
    st.markdown(f"### 🎨 {t('theme_toggle')}")
    tema_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    tema_text = t('dark_mode') if st.session_state.theme == 'light' else t('light_mode')
    
    if st.button(f"{tema_icon} {tema_text}", use_container_width=True):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.rerun()
    
    st.markdown("---")
    
    st.markdown(f"### {t('global_filters')}")
    
    # Métricas de resumen en sidebar
    st.markdown(f"""
    <div style="background: {COLORS['background']}; padding: 1rem; border-radius: 12px; margin: 1rem 0;">
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem;">{t('transactions')}</p>
        <p style="margin: 0; font-size: 1.3rem; font-weight: 700; color: {COLORS['primary']};">{metadata['total_transacciones']:,}</p>
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem; margin-top: 0.5rem;">{t('customers')}</p>
        <p style="margin: 0; font-size: 1.1rem; color: {COLORS['info']};">{metadata['total_clientes']:,}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de período
    st.markdown(t('period_filter'))
    
    fecha_min = metadata['fecha_min'].date()
    fecha_max = metadata['fecha_max'].date()
    
    rango_fechas = st.date_input(
        t('date_range'),
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
        help=t('tooltip_date_range')
    )
    
    if len(rango_fechas) == 2:
        fecha_inicio, fecha_fin = rango_fechas
    else:
        fecha_inicio, fecha_fin = fecha_min, fecha_max
    
    # Selector de países
    if not df_regiones.empty and 'Country' in df_regiones.columns:
        st.markdown(t('countries'))
        paises_disponibles = [t('all_countries')] + sorted(df_regiones['Country'].unique().tolist())
        pais_seleccionado = st.selectbox(
            t('select_country'),
            paises_disponibles,
            help=t('tooltip_country')
        )
    else:
        pais_seleccionado = t('all_countries')
    
    # Umbral de ventas
    st.markdown(t('sales_threshold'))
    umbral_ventas = st.slider(
        t('show_products'),
        min_value=0,
        max_value=50000,
        value=10000,
        step=1000,
        format="£%d"
    )
    
    st.markdown("---")
    
    # Botón de exportación
    if st.button(t('generate_pdf'), use_container_width=True):
        with st.spinner(t('generating')):
            st.success(t('report_ready'))
    
    st.markdown("---")
    
    # Badges de estado
    st.markdown(f"""
    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0;">
        <span class="badge badge-success">{t('updated')}</span>
        <span class="badge badge-info">{t('records')}</span>
    </div>
    
    <p style="color: {COLORS['text_secondary']}; font-size: 0.8rem; text-align: center; margin-top: 2rem;">
        Data Analyst: José Granado<br>
        v2.0 · {t('last_update')} {datetime.now().strftime('%d/%m/%Y')}
    </p>
    """, unsafe_allow_html=True)

# ============================================
# HEADER PRINCIPAL
# ============================================

col_title, col_date = st.columns([3, 1])

with col_title:
    st.markdown(f"""
    <h1 style="color: {COLORS['primary']}; margin: 0;">
        {t('title')}
    </h1>
    <p style="color: {COLORS['text_secondary']}; font-size: 1.1rem; margin-top: 0.3rem;">
        {t('subtitle')}
    </p>
    """, unsafe_allow_html=True)

with col_date:
    st.markdown(f"""
    <div style="background: {COLORS['card_bg']}; padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid {COLORS['border']};">
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem;">{t('period')}</p>
        <p style="margin: 0; color: {COLORS['primary']}; font-weight: 600;">
            {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# MÉTRICAS PRINCIPALES
# ============================================

if not df_problemas.empty:
    total_perdida = df_problemas['total_perdida'].sum()
    total_ventas = df_regiones['ventas_totales'].sum() if not df_regiones.empty else 0
    pct_perdida = (total_perdida / total_ventas * 100) if total_ventas > 0 else 0

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

with col_m1:
    st.metric(
        t('revenue_risk'),
        f"£{total_perdida:,.0f}",
        delta=f"{pct_perdida:.1f}% {t('of_total')}",
        delta_color="inverse",
        help=t('tooltip_revenue_risk')
    )

with col_m2:
    num_vip = len(df_clientes[df_clientes['categoria_cliente'] == '💎 VIP']) if not df_clientes.empty else 0
    pct_vip = (num_vip / len(df_clientes) * 100) if not df_clientes.empty and len(df_clientes) > 0 else 0
    st.metric(
        t('vip_customers'),
        f"{num_vip:,}",
        delta=f"{pct_vip:.1f}% {t('of_total')}",
        help=t('tooltip_vip')
    )

with col_m3:
    if not df_regiones.empty:
        top_pais = df_regiones.iloc[0]['Country']
        ventas_top = df_regiones.iloc[0]['ventas_totales']
        pct_top = (ventas_top / df_regiones['ventas_totales'].sum() * 100)
        st.metric(
            t('main_market'),
            top_pais,
            delta=f"{pct_top:.1f}% {t('of_total')}",
            help=t('tooltip_main_market')
        )
    else:
        st.metric(t('main_market'), "N/A")

with col_m4:
    num_productos_problema = len(df_problemas) if not df_problemas.empty else 0
    st.metric(
        t('problem_products'),
        f"{num_productos_problema:,}",
        help=t('tooltip_problem_products')
    )

with col_m5:
    st.metric(
        t('avg_ticket'),
        f"£{df_ticket['ticket_promedio'].mean():.2f}" if not df_ticket.empty else "N/A",
        help=t('tooltip_avg_ticket')
    )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# TABS PRINCIPALES
# ============================================

tab_overview, tab_products, tab_customers, tab_geography, tab_insights = st.tabs([
    t('tab_overview'),
    t('tab_products'),
    t('tab_customers'),
    t('tab_geography'),
    t('tab_insights')
])

# ============================================
# TAB 1: VISIÓN GENERAL
# ============================================

with tab_overview:
    st.markdown(t('kpi_trends'))
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        if not df_top_productos.empty:
            fig_top = px.bar(
                df_top_productos.head(10),
                x='revenue_total',
                y='Description',
                orientation='h',
                title=t('top_products'),
                labels={'revenue_total': 'Ingresos (£)' if st.session_state.language == 'es' else 'Revenue (£)', 'Description': ''},
                color='revenue_total',
                color_continuous_scale=[COLORS['gradient_start'], COLORS['gradient_end']],
                text='revenue_total'
            )
            
            fig_top.update_traces(
                texttemplate='£%{text:,.0f}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig_top.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_top, use_container_width=True)
    
    with col_right:
        if not df_regiones.empty:
            perf_counts = df_regiones['performance'].value_counts().reset_index()
            perf_counts.columns = ['performance', 'count']
            
            colors_map = {
                '🔥 Excelente': COLORS['success'],
                '👍 Bueno': COLORS['info'],
                '⚠️ Bajo': COLORS['warning']
            }
            
            fig_perf = px.pie(
                perf_counts,
                values='count',
                names='performance',
                title=t('performance_dist'),
                color='performance',
                color_discrete_map=colors_map,
                hole=0.4
            )
            
            fig_perf.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='white', width=2))
            )
            fig_perf.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_perf, use_container_width=True)
    
    with st.expander(t('view_full_table'), expanded=False):
        if not df_top_productos.empty:
            df_display = df_top_productos.copy()
            df_display['revenue_total'] = df_display['revenue_total'].apply(lambda x: f"£{x:,.2f}")
            df_display.columns = [t('product'), t('total_revenue'), t('units_sold')]
            st.dataframe(df_display, hide_index=True, use_container_width=True)

# ============================================
# TAB 2: ANÁLISIS DE PRODUCTOS
# ============================================

with tab_products:
    st.markdown(t('detailed_analysis'))
    
    col_prob, col_success = st.columns([1, 1])
    
    with col_prob:
        st.markdown(f"""
        <div class="insight-card warning">
            <h4 style="margin: 0 0 0.5rem 0; color: {COLORS['warning']};">🚨 {t('problematic_products')}</h4>
            <p style="margin: 0; font-size: 2rem; font-weight: 700;">£{total_perdida:,.0f}</p>
            <p style="color: {COLORS['text_secondary']};">{t('uncategorized_revenue')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not df_problemas.empty:
            fig_problemas = px.bar(
                df_problemas.head(10),
                x='total_perdida',
                y='Description',
                orientation='h',
                title=t('top_10_problematic'),
                labels={'total_perdida': 'Ingresos (£)' if st.session_state.language == 'es' else 'Revenue (£)', 'Description': ''},
                color='total_perdida',
                color_continuous_scale='Reds',
                text='total_perdida'
            )
            
            fig_problemas.update_traces(
                texttemplate='£%{text:,.0f}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig_problemas.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_problemas, use_container_width=True)
    
    with col_success:
        st.markdown(f"""
        <div class="insight-card success">
            <h4 style="margin: 0 0 0.5rem 0; color: {COLORS['success']};">{t('top_performers')}</h4>
            <p style="margin: 0; font-size: 2rem; font-weight: 700;">{len(df_top_productos) if not df_top_productos.empty else 0}</p>
            <p style="color: {COLORS['text_secondary']};">{t('high_performance')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not df_top_productos.empty:
            fig_success = px.bar(
                df_top_productos.head(10),
                x='revenue_total',
                y='Description',
                orientation='h',
                title=t('top_10_revenue'),
                labels={'revenue_total': 'Ingresos (£)' if st.session_state.language == 'es' else 'Revenue (£)', 'Description': ''},
                color='revenue_total',
                color_continuous_scale='Greens',
                text='revenue_total'
            )
            
            fig_success.update_traces(
                texttemplate='£%{text:,.0f}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig_success.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_success, use_container_width=True)
    
    st.markdown(t('performance_comparison'))
    
    if not df_top_productos.empty and not df_problemas.empty:
        col_comp1, col_comp2, col_comp3 = st.columns(3)
        
        with col_comp1:
            avg_success = df_top_productos['revenue_total'].mean()
            st.markdown(f"""
            <div style="background: {COLORS['card_bg']}; padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid {COLORS['border']};">
                <p style="color: {COLORS['text_secondary']}; margin: 0;">{t('avg_top_products')}</p>
                <p style="color: {COLORS['success']}; font-size: 1.5rem; font-weight: 700; margin: 0;">£{avg_success:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_comp2:
            avg_problem = df_problemas['total_perdida'].mean()
            st.markdown(f"""
            <div style="background: {COLORS['card_bg']}; padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid {COLORS['border']};">
                <p style="color: {COLORS['text_secondary']}; margin: 0;">{t('avg_problematic')}</p>
                <p style="color: {COLORS['warning']}; font-size: 1.5rem; font-weight: 700; margin: 0;">£{avg_problem:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_comp3:
            ratio = (avg_success / avg_problem) if avg_problem > 0 else 0
            st.markdown(f"""
            <div style="background: {COLORS['card_bg']}; padding: 1rem; border-radius: 12px; text-align: center; border: 1px solid {COLORS['border']};">
                <p style="color: {COLORS['text_secondary']}; margin: 0;">{t('efficiency_ratio')}</p>
                <p style="color: {COLORS['primary']}; font-size: 1.5rem; font-weight: 700; margin: 0;">{ratio:.1f}x</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 3: SEGMENTACIÓN CLIENTES
# ============================================

with tab_customers:
    st.markdown(t('customer_analysis'))
    
    if not df_clientes.empty:
        col_viz1, col_viz2 = st.columns([1, 1])
        
        with col_viz1:
            cat_counts = df_clientes['categoria_cliente'].value_counts().reset_index()
            cat_counts.columns = ['Categoría', 'Cantidad']
            
            fig_cat = px.pie(
                cat_counts,
                values='Cantidad',
                names='Categoría',
                title=t('category_distribution'),
                color='Categoría',
                color_discrete_map={
                    '💎 VIP': COLORS['success'],
                    '🌟 Premium': COLORS['info'],
                    '🔄 Regular': COLORS['secondary'],
                    '⚠️ Bajo': COLORS['warning']
                },
                hole=0.4
            )
            
            fig_cat.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='white', width=2))
            )
            fig_cat.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        
        with col_viz2:
            cat_value = df_clientes.groupby('categoria_cliente')['total_gastado'].sum().reset_index()
            cat_value.columns = ['Categoría', 'Valor']
            
            fig_value = px.bar(
                cat_value,
                x='Categoría',
                y='Valor',
                title=t('value_by_category'),
                color='Categoría',
                color_discrete_map={
                    '💎 VIP': COLORS['success'],
                    '🌟 Premium': COLORS['info'],
                    '🔄 Regular': COLORS['secondary'],
                    '⚠️ Bajo': COLORS['warning']
                },
                text='Valor'
            )
            
            fig_value.update_traces(
                texttemplate='£%{text:,.0f}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig_value.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis_title=""
            )
            st.plotly_chart(fig_value, use_container_width=True)
        
        st.markdown(t('top_10_vip'))
        
        top_vip = df_clientes[df_clientes['categoria_cliente'] == '💎 VIP'].nlargest(10, 'total_gastado')
        
        if not top_vip.empty:
            vip_display = []
            for idx, row in top_vip.iterrows():
                vip_display.append({
                    'Customer ID': int(row['Customer ID']) if pd.notna(row['Customer ID']) else 'N/A',
                    'Total Gastado': f"£{row['total_gastado']:,.2f}",
                    'Categoría': row['categoria_cliente']
                })
            
            df_vip_display = pd.DataFrame(vip_display)
            
            for i in range(0, len(df_vip_display), 2):
                col1, col2 = st.columns(2)
                if i < len(df_vip_display):
                    with col1:
                        st.markdown(f"""
                        <div style="background: {COLORS['card_bg']}; padding: 1rem; border-radius: 12px; margin: 0.5rem 0; border: 1px solid {COLORS['border']};">
                            <span class="badge badge-success">#{i+1}</span>
                            <p style="font-weight: 600; margin: 0.5rem 0; color: {COLORS['text']};">ID: {df_vip_display.iloc[i]['Customer ID']}</p>
                            <p style="color: {COLORS['success']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{df_vip_display.iloc[i]['Total Gastado']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if i+1 < len(df_vip_display):
                    with col2:
                        st.markdown(f"""
                        <div style="background: {COLORS['card_bg']}; padding: 1rem; border-radius: 12px; margin: 0.5rem 0; border: 1px solid {COLORS['border']};">
                            <span class="badge badge-success">#{i+2}</span>
                            <p style="font-weight: 600; margin: 0.5rem 0; color: {COLORS['text']};">ID: {df_vip_display.iloc[i+1]['Customer ID']}</p>
                            <p style="color: {COLORS['success']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{df_vip_display.iloc[i+1]['Total Gastado']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info(t('no_vip'))

# ============================================
# TAB 4: GEOGRAFÍA
# ============================================

with tab_geography:
    st.markdown(t('geo_analysis'))
    
    if not df_regiones.empty:
        col_map, col_stats = st.columns([2, 1])
        
        with col_map:
            fig_geo = px.bar(
                df_regiones.head(20),
                x='ventas_totales',
                y='Country',
                orientation='h',
                title=t('top_20_countries'),
                labels={'ventas_totales': 'Ventas (£)' if st.session_state.language == 'es' else 'Sales (£)', 'Country': ''},
                color='ventas_totales',
                color_continuous_scale=[COLORS['gradient_start'], COLORS['gradient_end']],
                text='ventas_totales'
            )
            
            fig_geo.update_traces(
                texttemplate='£%{text:,.0f}',
                textposition='outside',
                marker=dict(line=dict(width=0))
            )
            fig_geo.update_layout(
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_geo, use_container_width=True)
        
        with col_stats:
            total_ventas_geo = df_regiones['ventas_totales'].sum()
            top3 = df_regiones.head(3)['ventas_totales'].sum()
            pct_top3 = (top3 / total_ventas_geo * 100) if total_ventas_geo > 0 else 0
            
            st.markdown(f"""
            <div class="insight-card info">
                <h4 style="margin: 0 0 0.5rem 0; color: {COLORS['info']};">{t('concentration')}</h4>
                <p style="margin: 0; font-size: 2rem; font-weight: 700;">{pct_top3:.1f}%</p>
                <p style="color: {COLORS['text_secondary']};">{t('in_top_3')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            perf_geo = df_regiones['performance'].value_counts()
            
            st.markdown(t('performance_by'))
            
            for perf, count in perf_geo.items():
                if perf == '🔥 Excelente':
                    color = COLORS['success']
                    perf_text = t('excellent')
                elif perf == '👍 Bueno':
                    color = COLORS['info']
                    perf_text = t('good')
                else:
                    color = COLORS['warning']
                    perf_text = t('poor')
                
                st.markdown(f"""
                <div style="margin: 0.5rem 0;">
                    <span style="color: {color};">{perf_text}</span>
                    <div style="background: {COLORS['border']}; height: 8px; border-radius: 4px; margin: 0.2rem 0;">
                        <div style="background: {color}; width: {(count/len(df_regiones)*100)}%; height: 8px; border-radius: 4px;"></div>
                    </div>
                    <span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">{count} {t('countries')} ({count/len(df_regiones)*100:.1f}%)</span>
                </div>
                """, unsafe_allow_html=True)
            
            if not df_ticket.empty:
                st.markdown(t('top_5_ticket'))
                
                top_ticket = df_ticket.nlargest(5, 'ticket_promedio')
                for _, row in top_ticket.iterrows():
                    st.markdown(f"""
                    <div style="background: {COLORS['card_bg']}; padding: 0.5rem 1rem; border-radius: 8px; margin: 0.3rem 0; border: 1px solid {COLORS['border']};">
                        <span style="font-weight: 600; color: {COLORS['text']};">{row['Country']}</span>
                        <span style="float: right; color: {COLORS['success']};">£{row['ticket_promedio']:.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ============================================
# TAB 5: INSIGHTS Y ACCIONES
# ============================================

with tab_insights:
    st.markdown(t('strategic_insights'))
    
    col_ins1, col_ins2, col_ins3 = st.columns(3)
    
    with col_ins1:
        st.markdown(f"""
        <div style="background: {COLORS['card_bg']}; padding: 1.5rem; border-radius: 16px; height: 100%; border: 1px solid {COLORS['border']};">
            <h4 style="color: {COLORS['warning']}; margin: 0 0 1rem 0;">{t('critical_risk')}</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['warning']}; margin: 0;">£{total_perdida:,.0f}</p>
            <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0 1rem 0;">{t('uncategorized_revenue_short')}</p>
            <hr style="border: none; border-top: 1px solid {COLORS['border']};">
            <p style="color: {COLORS['text']}; font-weight: 500;">{t('immediate_action')}</p>
            <ul style="color: {COLORS['text_secondary']};">
                <li>{t('action_catalog')}</li>
                <li>{t('action_naming')}</li>
                <li>{t('action_validation')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ins2:
        st.markdown(f"""
        <div style="background: {COLORS['card_bg']}; padding: 1.5rem; border-radius: 16px; height: 100%; border: 1px solid {COLORS['border']};">
            <h4 style="color: {COLORS['success']}; margin: 0 0 1rem 0;">{t('vip_opportunity')}</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['success']}; margin: 0;">{num_vip}</p>
            <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0 1rem 0;">{t('high_value_customers')}</p>
            <hr style="border: none; border-top: 1px solid {COLORS['border']};">
            <p style="color: {COLORS['text']}; font-weight: 500;">{t('retention_program')}</p>
            <ul style="color: {COLORS['text_secondary']};">
                <li>{t('action_discounts')}</li>
                <li>{t('action_early_access')}</li>
                <li>{t('action_support')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_ins3:
        st.markdown(f"""
        <div style="background: {COLORS['card_bg']}; padding: 1.5rem; border-radius: 16px; height: 100%; border: 1px solid {COLORS['border']};">
            <h4 style="color: {COLORS['info']}; margin: 0 0 1rem 0;">{t('expansion')}</h4>
            <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['info']}; margin: 0;">{pct_top3:.0f}%</p>
            <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0 1rem 0;">{t('concentration_top3')}</p>
            <hr style="border: none; border-top: 1px solid {COLORS['border']};">
            <p style="color: {COLORS['text']}; font-weight: 500;">{t('diversification')}</p>
            <ul style="color: {COLORS['text_secondary']};">
                <li>{t('action_secondary')}</li>
                <li>{t('action_campaigns')}</li>
                <li>{t('action_logistics')}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(t('recommended_plan'))
    
    acciones = [
        {
            "prioridad": t('high_priority'),
            "accion": t('action_catalog'),
            "impacto": t('impact_recoverable'),
            "plazo": "1 mes"
        },
        {
            "prioridad": t('medium_priority'),
            "accion": t('action_discounts'),
            "impacto": t('impact_retention'),
            "plazo": "3 meses"
        },
        {
            "prioridad": t('medium_priority'),
            "accion": t('action_secondary'),
            "impacto": t('impact_new_revenue'),
            "plazo": "6 meses"
        },
        {
            "prioridad": t('low_priority'),
            "accion": t('action_automation'),
            "impacto": t('impact_efficiency'),
            "plazo": "2 meses"
        }
    ]
    
    for accion in acciones:
        if accion["prioridad"] == t('high_priority'):
            color = COLORS['warning']
            bg_color = "rgba(239, 68, 68, 0.1)"
        elif accion["prioridad"] == t('medium_priority'):
            color = COLORS['info']
            bg_color = "rgba(59, 130, 246, 0.1)"
        else:
            color = COLORS['secondary']
            bg_color = "rgba(245, 158, 11, 0.1)"
        
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1rem 1.5rem; border-radius: 12px; margin: 0.5rem 0; border: 1px solid {color}40;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background: {color}; color: white; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{accion['prioridad']}</span>
                    <span style="font-weight: 600; margin-left: 1rem; color: {COLORS['text']};">{accion['accion']}</span>
                </div>
                <div style="color: {color}; font-weight: 600;">
                    {accion['impacto']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; padding: 2rem 0;">
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem;">
        <span class="badge badge-info">Python 3.9+</span>
        <span class="badge badge-info">Streamlit 1.28+</span>
        <span class="badge badge-info">SQLite 3</span>
        <span class="badge badge-info">Plotly</span>
    </div>
    <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
        <strong>Retail UK Analytics Dashboard</strong> · {t('developed_by')}<br>
        {t('dataset')} · 1.7M transacciones · {t('tools')}<br>
        {datetime.now().strftime('%Y')} · {t('rights')}
    </p>
</div>
""", unsafe_allow_html=True)