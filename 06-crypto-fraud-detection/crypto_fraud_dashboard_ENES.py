import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="Crypto Fraud · Blockchain Security",
    page_icon="🔐",
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
        'title': 'Crypto Fraud Detection System',
        'subtitle': 'Blockchain Security · ML-Powered Analytics',
        'period': 'Analysis period',
        
        # Metrics
        'accounts_analyzed': '🔍 ACCOUNTS ANALYZED',
        'fraud_detected': '🚨 FRAUD DETECTED',
        'bots_identified': '⚡ BOTS IDENTIFIED',
        'tokens_at_risk': '🪙 TOKENS AT RISK',
        'unique_ethereum': 'Unique Ethereum addresses',
        'confirmed_fraud': 'Confirmed fraudulent accounts',
        'bot_behavior': 'Accounts with automated behavior',
        'high_fraud_tokens': 'Tokens with high fraud rate',
        
        # Sidebar
        'language': '🌐 Language',
        'theme': '🎨 Theme',
        'dark_mode': '🌙 Dark Mode',
        'light_mode': '☀️ Light Mode',
        'filters': '🔍 Filters',
        'transactions': '📦 Transactions',
        'addresses': '👥 Addresses',
        'period_filter': '#### 📅 Period',
        'date_range': 'Date range',
        'risk_level': '#### ⚠️ Risk Level',
        'select_risk': 'Select risk level',
        'all_levels': 'All',
        'threshold': '#### 🔢 Minimum transactions',
        'show_addresses': 'Show addresses with txs >',
        'generate_report': '📥 Generate Report',
        'generating': 'Generating report...',
        'report_ready': 'Report generated! (Demo)',
        'updated': '● Data updated',
        'records': '● 9.8K records',
        'last_update': 'Last update:',
        
        # Tabs
        'tab_risk_profile': '📊 Risk Profile',
        'tab_bot_detection': '⚡ Bot Detection',
        'tab_volume': '💰 Volume Analysis',
        'tab_tokens': '🪙 Suspicious Tokens',
        'tab_ghost': '👻 Ghost Accounts',
        'tab_scoring': '🎯 Scoring System',
        
        # Risk Profile tab
        'behavior_profile': 'Behavior Profile',
        'time_between_sends': 'Time Between Sends (min)',
        'erc20_transactions': 'ERC20 Transactions',
        'time_between_receives': 'Time Between Receives (min)',
        'legitimate': 'Legitimate',
        'fraud': 'Fraud',
        'legitimate_accounts': '✅ Legitimate Accounts',
        'fraud_accounts': '❌ Fraudulent Accounts',
        'legit_features': ['Longer time between transactions', 'Moderate ERC20 activity', '"Human" behavior'],
        'fraud_features': ['High transaction speed', 'Clear automation', 'Confirmed bot patterns'],
        
        # Bot Detection tab
        'bot_detection': 'Bot Detection by Speed',
        'speed_distribution': 'Speed Distribution by Account Type',
        'accounts': 'Number of Accounts',
        'speed_category': 'Transaction Speed',
        'details_by_category': '📋 Details by Category',
        'total': 'Total',
        'fraud_percent': '% Fraud',
        
        # Volume Analysis tab
        'volume_analysis': 'Ether Volume Analysis',
        'avg_sent': 'Average Sent',
        'max_sent': 'Maximum Sent',
        'comparison': 'Ether Volume Comparison',
        'eth': 'ETH',
        'account_type': 'Account Type',
        'counterintuitive': '💡 Counterintuitive Insight',
        'fraud_move_less': 'Fraudulent accounts move',
        'times_less_eth': 'times less ETH than legitimate ones',
        'legit_avg': 'Legitimate average',
        'fraud_avg': 'Fraud average',
        'small_volumes': 'Fraud operates in small volumes but high frequency',
        'volume_table': '📊 Volume Table',
        'type': 'Type',
        'min_eth': 'Min ETH',
        'avg_eth': 'Avg ETH',
        'max_eth': 'Max ETH',
        'total_volume': 'Total Volume ETH',
        
        # Suspicious Tokens tab
        'suspicious_tokens': 'Top Suspicious Tokens',
        'tokens_highest_fraud': 'Tokens with Highest Fraud Index',
        'fraud_cases': 'Fraud Cases',
        'token': 'Token',
        'token_details': '📋 Token Details',
        'mentions': 'Mentions',
        'fraud_cases_count': 'Fraud Cases',
        'fraud_rate': 'Fraud Rate (%)',
        'most_dangerous': '⚠️ Most Dangerous Token',
        'action_blacklist': 'Immediate blacklist',
        'no_token_data': 'No token data available',
        
        # Ghost Accounts tab
        'ghost_accounts': 'Ghost Accounts (Zero Balance)',
        'zero_balance_dist': 'Accounts with Balance = 0 Distribution',
        'pattern_identified': '💡 Identified Pattern',
        'ghost_description': 'Accounts with zero balance are typically:',
        'ghost_features': ['Disposable accounts (use and discard)', 'Spam bots', 'Honey pots (traps to receive funds)'],
        'recommendation': 'Special monitoring for accounts with balance < 0.01 ETH',
        'no_vulnerability': 'No vulnerability data available',
        'demo_data': '📊 **Demo Data - Showing sample distribution**',
        
        # Scoring System tab
        'scoring_system': 'Risk Scoring System',
        'risk_factors': 'Risk Factors Identified',
        'factor': 'Factor',
        'weight': 'Weight',
        'criteria': 'Criteria',
        'instant_txs': '⚡ Instant transactions',
        'instant_criteria': '< 1 min between sends',
        'only_sends': '📤 Only sends (no receives)',
        'only_sends_criteria': '0 receives + >10 sends',
        'high_activity': '🔥 High activity',
        'high_activity_criteria': '>1000 transactions',
        'extreme_ratio': '📊 Extreme ratio',
        'extreme_ratio_criteria': 'Sends/Receives > 10x',
        'many_contracts': '📝 Many contracts',
        'many_contracts_criteria': '>5 contracts created',
        'risk_classification': 'Risk Classification',
        'high_risk': '🔴 High Risk',
        'medium_risk': '🟠 Medium Risk',
        'low_risk': '🟡 Low Risk',
        'no_risk': '🟢 No Risk',
        'points': 'points',
        'fraud_rate_text': 'fraud rate',
        
        # Action Plan
        'action_plan': 'Action Plan',
        'immediate': '🚨 IMMEDIATE',
        'this_week': 'This Week',
        'actions_immediate': ['Blacklist top 5 tokens', 'Score ≥8: Auto-block', 'Daily manual review'],
        'short_term': '⚡ SHORT TERM',
        'this_month': 'This Month',
        'actions_short': ['Real-time alerts', 'Improve ML model', 'Add new features'],
        'medium_term': '🎯 MEDIUM TERM',
        'this_quarter': 'This Quarter',
        'actions_medium': ['Graph network analysis', 'Share blacklists', 'Common database'],
        
        # Footer
        'developed_by': 'Crafted by José Granado',
        'tools': 'Tools: SQL + Python + Streamlit',
        'rights': 'Securing the blockchain, one address at a time',
        'style': 'ML-Powered',
        
        # Tooltips
        'tooltip_accounts': 'Unique Ethereum addresses',
        'tooltip_fraud': 'Confirmed fraudulent accounts',
        'tooltip_bots': 'Accounts with automated behavior',
        'tooltip_tokens': 'Tokens with high fraud rate',
        'tooltip_date_range': 'Filter data by date',
        'tooltip_risk': 'Filter by risk level',
    },
    'es': {
        # Header
        'title': 'Sistema de Detección de Fraude Crypto',
        'subtitle': 'Seguridad Blockchain · Analítica con ML',
        'period': 'Período analizado',
        
        # Metrics
        'accounts_analyzed': '🔍 CUENTAS ANALIZADAS',
        'fraud_detected': '🚨 FRAUDE DETECTADO',
        'bots_identified': '⚡ BOTS IDENTIFICADOS',
        'tokens_at_risk': '🪙 TOKENS EN RIESGO',
        'unique_ethereum': 'Direcciones Ethereum únicas',
        'confirmed_fraud': 'Cuentas fraudulentas confirmadas',
        'bot_behavior': 'Cuentas con comportamiento automatizado',
        'high_fraud_tokens': 'Tokens con alto índice de fraude',
        
        # Sidebar
        'language': '🌐 Idioma',
        'theme': '🎨 Tema',
        'dark_mode': '🌙 Modo Oscuro',
        'light_mode': '☀️ Modo Claro',
        'filters': '🔍 Filtros',
        'transactions': '📦 Transacciones',
        'addresses': '👥 Direcciones',
        'period_filter': '#### 📅 Período',
        'date_range': 'Rango de fechas',
        'risk_level': '#### ⚠️ Nivel de Riesgo',
        'select_risk': 'Seleccionar nivel',
        'all_levels': 'Todos',
        'threshold': '#### 🔢 Transacciones mínimas',
        'show_addresses': 'Mostrar direcciones con txs >',
        'generate_report': '📥 Generar Reporte',
        'generating': 'Generando reporte...',
        'report_ready': '¡Reporte generado! (Demo)',
        'updated': '● Datos actualizados',
        'records': '● 9.8K registros',
        'last_update': 'Última actualización:',
        
        # Tabs
        'tab_risk_profile': '📊 Perfil de Riesgo',
        'tab_bot_detection': '⚡ Detección de Bots',
        'tab_volume': '💰 Análisis de Volumen',
        'tab_tokens': '🪙 Tokens Sospechosos',
        'tab_ghost': '👻 Cuentas Fantasma',
        'tab_scoring': '🎯 Sistema de Scoring',
        
        # Risk Profile tab
        'behavior_profile': 'Perfil de Comportamiento',
        'time_between_sends': 'Tiempo entre Envíos (min)',
        'erc20_transactions': 'Transacciones ERC20',
        'time_between_receives': 'Tiempo entre Recepciones (min)',
        'legitimate': 'Legítimo',
        'fraud': 'Fraude',
        'legitimate_accounts': '✅ Cuentas Legítimas',
        'fraud_accounts': '❌ Cuentas Fraudulentas',
        'legit_features': ['Mayor tiempo entre transacciones', 'Actividad ERC20 moderada', 'Comportamiento "humano"'],
        'fraud_features': ['Velocidad de transacción alta', 'Automatización evidente', 'Patrones de bot confirmados'],
        
        # Bot Detection tab
        'bot_detection': 'Detección de Bots por Velocidad',
        'speed_distribution': 'Distribución de Velocidad por Tipo de Cuenta',
        'accounts': 'Cantidad de Cuentas',
        'speed_category': 'Velocidad de Transacción',
        'details_by_category': '📋 Detalle por Categoría',
        'total': 'Total',
        'fraud_percent': '% Fraude',
        
        # Volume Analysis tab
        'volume_analysis': 'Análisis de Volumen de Ether',
        'avg_sent': 'Promedio Enviado',
        'max_sent': 'Máximo Enviado',
        'comparison': 'Comparación de Volumen de Ether Enviado',
        'eth': 'ETH',
        'account_type': 'Tipo de Cuenta',
        'counterintuitive': '💡 Insight Contraintuitivo',
        'fraud_move_less': 'Las cuentas fraudulentas mueven',
        'times_less_eth': 'veces menos ETH que las legítimas',
        'legit_avg': 'Legítimo promedio',
        'fraud_avg': 'Fraude promedio',
        'small_volumes': 'El fraude opera en volúmenes pequeños pero alta frecuencia',
        'volume_table': '📊 Tabla de Volumen',
        'type': 'Tipo',
        'min_eth': 'Mín ETH',
        'avg_eth': 'Promedio ETH',
        'max_eth': 'Máx ETH',
        'total_volume': 'Volumen Total ETH',
        
        # Suspicious Tokens tab
        'suspicious_tokens': 'Top Tokens Sospechosos',
        'tokens_highest_fraud': 'Tokens con Mayor Índice de Fraude',
        'fraud_cases': 'Casos de Fraude',
        'token': 'Token',
        'token_details': '📋 Detalle de Tokens',
        'mentions': 'Menciones',
        'fraud_cases_count': 'Casos Fraude',
        'fraud_rate': 'Tasa Fraude (%)',
        'most_dangerous': '⚠️ Token Más Peligroso',
        'action_blacklist': 'Blacklist inmediata',
        'no_token_data': 'No hay datos de tokens disponibles',
        
        # Ghost Accounts tab
        'ghost_accounts': 'Cuentas Fantasma (Balance Cero)',
        'zero_balance_dist': 'Distribución de Cuentas con Balance = 0',
        'pattern_identified': '💡 Patrón Identificado',
        'ghost_description': 'Las cuentas con balance cero son típicamente:',
        'ghost_features': ['Cuentas descartables (usar y tirar)', 'Bots de spam', 'Honey pots (trampa para recibir fondos)'],
        'recommendation': 'Monitoreo especial en cuentas con balance < 0.01 ETH',
        'no_vulnerability': 'No hay datos de vulnerabilidad disponibles',
        'demo_data': '📊 **Datos de Demostración - Mostrando distribución de ejemplo**',
        
        # Scoring System tab
        'scoring_system': 'Sistema de Scoring de Riesgo',
        'risk_factors': 'Factores de Riesgo Identificados',
        'factor': 'Factor',
        'weight': 'Peso',
        'criteria': 'Criterio',
        'instant_txs': '⚡ Transacciones instantáneas',
        'instant_criteria': '< 1 min entre envíos',
        'only_sends': '📤 Solo envía (no recibe)',
        'only_sends_criteria': '0 recepciones + >10 envíos',
        'high_activity': '🔥 Alta actividad',
        'high_activity_criteria': '>1000 transacciones',
        'extreme_ratio': '📊 Ratio extremo',
        'extreme_ratio_criteria': 'Envíos/Recepciones > 10x',
        'many_contracts': '📝 Muchos contratos',
        'many_contracts_criteria': '>5 contratos creados',
        'risk_classification': 'Clasificación de Riesgo',
        'high_risk': '🔴 Alto Riesgo',
        'medium_risk': '🟠 Medio Riesgo',
        'low_risk': '🟡 Bajo Riesgo',
        'no_risk': '🟢 Sin Riesgo',
        'points': 'puntos',
        'fraud_rate_text': 'fraude',
        
        # Action Plan
        'action_plan': 'Plan de Acción',
        'immediate': '🚨 INMEDIATO',
        'this_week': 'Esta Semana',
        'actions_immediate': ['Blacklist top 5 tokens', 'Score ≥8: Auto-block', 'Revisión manual diaria'],
        'short_term': '⚡ CORTO PLAZO',
        'this_month': 'Este Mes',
        'actions_short': ['Alertas en tiempo real', 'Mejorar modelo ML', 'Incorporar nuevas features'],
        'medium_term': '🎯 MEDIANO PLAZO',
        'this_quarter': 'Este Trimestre',
        'actions_medium': ['Graph analysis de redes', 'Compartir blacklists', 'Base de datos común'],
        
        # Footer
        'developed_by': 'Creado por José Granado',
        'tools': 'Herramientas: SQL + Python + Streamlit',
        'rights': 'Asegurando la blockchain, una dirección a la vez',
        'style': 'ML-Powered',
        
        # Tooltips
        'tooltip_accounts': 'Direcciones Ethereum únicas',
        'tooltip_fraud': 'Cuentas fraudulentas confirmadas',
        'tooltip_bots': 'Cuentas con comportamiento automatizado',
        'tooltip_tokens': 'Tokens con alto índice de fraude',
        'tooltip_date_range': 'Filtra datos por fecha',
        'tooltip_risk': 'Filtra por nivel de riesgo',
    }
}

# Función helper para textos
def t(key):
    """Retorna texto en el idioma actual"""
    return TEXTS[st.session_state.language].get(key, key)

# ============================================
# PALETA DE COLORES CRYPTO
# ============================================
COLORS = {
    'primary': '#8B5CF6',      # Morado crypto
    'secondary': '#F59E0B',     # Naranja
    'success': '#10B981',        # Verde esmeralda
    'warning': '#EF4444',        # Rojo
    'info': '#3B82F6',           # Azul
    'purple_dark': '#6D28D9',    # Morado oscuro
    'purple_light': '#A78BFA',   # Morado claro
    'background': '#0A0A0F' if st.session_state.theme == 'dark' else '#F8FAFC',
    'card_bg': '#1A1A23' if st.session_state.theme == 'dark' else '#FFFFFF',
    'text': '#FFFFFF' if st.session_state.theme == 'dark' else '#0F172A',
    'text_secondary': '#A0A0B0' if st.session_state.theme == 'dark' else '#475569',
    'border': '#2A2A35' if st.session_state.theme == 'dark' else '#E2E8F0'
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
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
    }}
    
    /* Tarjetas de métricas */
    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, {COLORS['card_bg']} 0%, {COLORS['card_bg']}dd 100%);
        padding: 1.5rem 1rem;
        border-radius: 20px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.2);
        transition: all 0.3s ease;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -10px rgba(139, 92, 246, 0.4);
        border-color: {COLORS['primary']};
    }}
    
    div[data-testid="stMetric"] label {{
        color: {COLORS['text_secondary']} !important;
        font-weight: 500 !important;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {COLORS['primary']} !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
        color: {COLORS['text_secondary']} !important;
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
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
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
    
    .badge-primary {{
        background: rgba(139, 92, 246, 0.15);
        color: {COLORS['primary']} !important;
        border: 1px solid {COLORS['primary']}40;
    }}
    
    /* Alert Cards */
    .alert-card {{
        background: {COLORS['card_bg']};
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    
    .alert-title {{
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        color: {COLORS['warning']} !important;
    }}
    
    /* DataFrames */
    .stDataFrame {{
        color: {COLORS['text']} !important;
    }}
    
    .stDataFrame td {{
        color: {COLORS['text']} !important;
    }}
    
    .stDataFrame th {{
        color: {COLORS['text']} !important;
        background-color: {COLORS['primary']}20 !important;
    }}
    
    /* Divider */
    .custom-divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, {COLORS['primary']} 50%, transparent 100%);
        margin: 2rem 0;
        opacity: 0.3;
    }}
    
    /* Gradient Header */
    .gradient-header {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['purple_light']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }}
    
    /* Captions */
    .stCaption {{
        color: {COLORS['text_secondary']} !important;
    }}
    
    /* Success/Error/Info boxes */
    .stSuccess, .stInfo, .stWarning, .stError {{
        color: {COLORS['text']} !important;
    }}
    
    div[data-testid="stNotification"] {{
        color: {COLORS['text']} !important;
    }}
    
    /* Plotly charts background */
    .js-plotly-plot {{
        background-color: transparent !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE CARGA
# ============================================
@st.cache_data(ttl=3600, show_spinner="🔗 Conectando a blockchain...")
def load_crypto_data(db_path):
    """Carga todas las tablas de crypto"""
    
    tables = {
        'perfil': "df_crypto_perfil_riesgo",
        'velocidad': "df_crypto_velocidad_bots",
        'volumen': "df_crypto_volumen_ether",
        'tokens': "df_crypto_tokens_sospechosos",
        'vulnerabilidad': "df_crypto_vulnerabilidad"
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
        st.error(f"💥 Error de conexión: {e}")
        return {}

# ============================================
# CARGA DE DATOS
# ============================================
DB_PATH = r"C:\Users\JOSE GRANADO PC\desktop\crypto-data\fraud_crypto.db"

with st.spinner("🔐 Analizando blockchain..."):
    data = load_crypto_data(DB_PATH)

if not data:
    st.error("❌ No se pudo conectar a la base de datos")
    st.stop()

df_perfil = data.get('perfil', pd.DataFrame())
df_velocidad = data.get('velocidad', pd.DataFrame())
df_volumen = data.get('volumen', pd.DataFrame())
df_tokens = data.get('tokens', pd.DataFrame())
df_vulnerabilidad = data.get('vulnerabilidad', pd.DataFrame())

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: {COLORS['primary']};">🔐 Crypto Fraud</h2>
        <p style="color: {COLORS['text_secondary']};">Security Analytics</p>
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
    
    # ===== FILTROS =====
    st.markdown(f"<h4 style='color: {COLORS['text']} !important;'>{t('filters')}</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: {COLORS['background']}; padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid {COLORS['border']};">
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem;">{t('addresses')}</p>
        <p style="margin: 0; font-size: 1.3rem; font-weight: 700; color: {COLORS['primary']};">9,841</p>
        <p style="margin: 0; color: {COLORS['text_secondary']}; font-size: 0.8rem; margin-top: 0.5rem;">{t('transactions')}</p>
        <p style="margin: 0; font-size: 1.1rem; color: {COLORS['info']};">1.2M</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
col_logo, col_title, col_toggle = st.columns([1, 3, 1])

with col_logo:
    st.markdown("""
    <div style="font-size: 3rem; text-align: center;">🔐</div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown(f"""
    <h1 style="margin: 0;">
        <span class="gradient-header">Crypto Fraud</span> <span style="color: {COLORS['text']};">{t('title').replace('Crypto Fraud ', '')}</span>
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
st.markdown(f"<h2>📊 <span class='gradient-header'>{t('accounts_analyzed')}</span></h2>", unsafe_allow_html=True)

# Calcular métricas
total_cuentas = df_perfil['total_cuentas'].sum() if not df_perfil.empty else 0
cuentas_fraude = df_perfil[df_perfil['es_fraude'] == 1]['total_cuentas'].values[0] if not df_perfil.empty and len(df_perfil[df_perfil['es_fraude'] == 1]) > 0 else 0
tasa_fraude = (cuentas_fraude / total_cuentas * 100) if total_cuentas > 0 else 0

bots = df_velocidad[df_velocidad['categoria_velocidad'].str.contains('Bot', na=False)]['cantidad_direcciones'].sum() if not df_velocidad.empty else 0
tokens_riesgo = len(df_tokens[df_tokens['casos_fraude_confirmados'] > 5]) if not df_tokens.empty else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        t('accounts_analyzed'),
        f"{total_cuentas:,}",
        help=t('tooltip_accounts')
    )

with col2:
    st.metric(
        t('fraud_detected'),
        f"{cuentas_fraude:,}",
        delta=f"{tasa_fraude:.1f}%",
        delta_color="inverse",
        help=t('tooltip_fraud')
    )

with col3:
    st.metric(
        t('bots_identified'),
        f"{bots:,.0f}",
        help=t('tooltip_bots')
    )

with col4:
    st.metric(
        t('tokens_at_risk'),
        tokens_riesgo,
        help=t('tooltip_tokens')
    )

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================
# ALERTA CRÍTICA
# ============================================
col_alert1, col_alert2 = st.columns([2, 1])

with col_alert1:
    st.markdown(f"""
    <div class="alert-card">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="font-size: 2rem;">🚨</span>
            <span class="badge badge-warning" style="font-size: 1rem;">{t('high_risk')}</span>
        </div>
        <h3 style="color: {COLORS['warning']};">Security Critical Findings</h3>
        <div style="display: flex; gap: 2rem; margin: 1.5rem 0;">
            <div>
                <p style="color: {COLORS['text_secondary']}; margin: 0;">Fraud rate</p>
                <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['warning']}; margin: 0;">{tasa_fraude:.1f}%</p>
            </div>
            <div>
                <p style="color: {COLORS['text_secondary']}; margin: 0;">{t('bots_identified')}</p>
                <p style="font-size: 2.5rem; font-weight: 700; color: {COLORS['primary']}; margin: 0;">{bots:,.0f}</p>
            </div>
        </div>
        <ul style="color: {COLORS['text_secondary']};">
            <li><strong style="color: {COLORS['warning']};">Main pattern:</strong> High frequency bots</li>
            <li><strong style="color: {COLORS['warning']};">Attack vector:</strong> Fake ERC20 tokens</li>
            <li><strong style="color: {COLORS['warning']};">Key indicator:</strong> Low balance + high speed</li>
        </ul>
        <p style="background: {COLORS['warning']}20; padding: 1rem; border-radius: 12px; color: {COLORS['text']};">
            <strong>Predictive model:</strong> 58% early detection accuracy
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_alert2:
    if total_cuentas > 0:
        fig_mini = px.pie(
            values=[cuentas_fraude, total_cuentas - cuentas_fraude],
            names=[t('fraud'), t('legitimate')],
            title="Account Distribution",
            color_discrete_sequence=[COLORS['warning'], COLORS['success']],
            hole=0.5
        )
        fig_mini.update_layout(
            height=300,
            showlegend=True,
            margin=dict(t=40, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        st.plotly_chart(fig_mini, use_container_width=True)

# ============================================
# TABS
# ============================================
tabs = st.tabs([
    t('tab_risk_profile'),
    t('tab_bot_detection'),
    t('tab_volume'),
    t('tab_tokens'),
    t('tab_ghost'),
    t('tab_scoring')
])

# ============================================
# TAB 1: PERFIL DE RIESGO
# ============================================
with tabs[0]:
    st.markdown(f"<h3><span class='gradient-header'>{t('behavior_profile')}</span></h3>", unsafe_allow_html=True)
    
    if not df_perfil.empty:
        df_perfil['tipo'] = df_perfil['es_fraude'].map({0: t('legitimate'), 1: t('fraud')})
        
        fig1 = make_subplots(
            rows=1, cols=3,
            subplot_titles=(t('time_between_sends'), t('erc20_transactions'), t('time_between_receives'))
        )
        
        # Gráfico 1
        fig1.add_trace(
            go.Bar(
                x=df_perfil['tipo'],
                y=df_perfil['promedio_tiempo_envio'],
                marker_color=[COLORS['success'], COLORS['warning']],
                text=df_perfil['promedio_tiempo_envio'].apply(lambda x: f'{x:.1f} min'),
                textposition='outside',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Gráfico 2
        fig1.add_trace(
            go.Bar(
                x=df_perfil['tipo'],
                y=df_perfil['promedio_transacciones_erc20'],
                marker_color=[COLORS['success'], COLORS['warning']],
                text=df_perfil['promedio_transacciones_erc20'].apply(lambda x: f'{x:.1f}'),
                textposition='outside',
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Gráfico 3
        fig1.add_trace(
            go.Bar(
                x=df_perfil['tipo'],
                y=df_perfil['promedio_tiempo_recibo'],
                marker_color=[COLORS['success'], COLORS['warning']],
                text=df_perfil['promedio_tiempo_recibo'].apply(lambda x: f'{x:.1f} min'),
                textposition='outside',
                showlegend=False
            ),
            row=1, col=3
        )
        
        fig1.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        col_legit, col_fraud = st.columns(2)
        
        with col_legit:
            legit_features = t('legit_features')
            if isinstance(legit_features, list):
                features_list = legit_features
            else:
                features_list = ['Longer time between transactions', 'Moderate ERC20 activity', '"Human" behavior']
            
            features_html = ''.join([f'<li>{f}</li>' for f in features_list])
            
            st.markdown(f"""
            <div style="background: {COLORS['success']}20; padding: 1rem; border-radius: 12px;">
                <h4 style="color: {COLORS['success']};">{t('legitimate_accounts')}</h4>
                <ul style="color: {COLORS['text']};">{features_html}</ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_fraud:
            fraud_features = t('fraud_features')
            if isinstance(fraud_features, list):
                features_list = fraud_features
            else:
                features_list = ['High transaction speed', 'Clear automation', 'Confirmed bot patterns']
            
            features_html = ''.join([f'<li>{f}</li>' for f in features_list])
            
            st.markdown(f"""
            <div style="background: {COLORS['warning']}20; padding: 1rem; border-radius: 12px;">
                <h4 style="color: {COLORS['warning']};">{t('fraud_accounts')}</h4>
                <ul style="color: {COLORS['text']};">{features_html}</ul>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 2: DETECCIÓN DE BOTS
# ============================================
with tabs[1]:
    st.markdown(f"<h3><span class='gradient-header'>{t('bot_detection')}</span></h3>", unsafe_allow_html=True)
    
    if not df_velocidad.empty:
        df_vel = df_velocidad.copy()
        df_vel['tipo'] = df_vel['es_fraude'].map({0: t('legitimate'), 1: t('fraud')})
        
        fig2 = px.bar(
            df_vel,
            x='categoria_velocidad',
            y='cantidad_direcciones',
            color='tipo',
            title=t('speed_distribution'),
            labels={'cantidad_direcciones': t('accounts'), 'categoria_velocidad': t('speed_category')},
            color_discrete_map={t('legitimate'): COLORS['success'], t('fraud'): COLORS['warning']},
            text='cantidad_direcciones',
            barmode='group'
        )
        
        fig2.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig2.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown(f"<h4 style='color: {COLORS['text']};'>{t('details_by_category')}</h4>", unsafe_allow_html=True)
        
        vel_display = df_vel.pivot(index='categoria_velocidad', columns='tipo', values='cantidad_direcciones').fillna(0)
        vel_display[t('total')] = vel_display.sum(axis=1)
        vel_display[t('fraud_percent')] = (vel_display[t('fraud')] / vel_display[t('total')] * 100).round(1)
        
        st.dataframe(
            vel_display.style.format({
                t('legitimate'): '{:.0f}',
                t('fraud'): '{:.0f}',
                t('total'): '{:.0f}',
                t('fraud_percent'): '{:.1f}%'
            }),
            use_container_width=True
        )

# ============================================
# TAB 3: ANÁLISIS DE VOLUMEN
# ============================================
with tabs[2]:
    st.markdown(f"<h3><span class='gradient-header'>{t('volume_analysis')}</span></h3>", unsafe_allow_html=True)
    
    if not df_volumen.empty:
        df_vol = df_volumen.copy()
        df_vol['tipo'] = df_vol['es_fraude'].map({0: t('legitimate'), 1: t('fraud')})
        
        fig3 = go.Figure()
        
        fig3.add_trace(go.Bar(
            name=t('avg_sent'),
            x=df_vol['tipo'],
            y=df_vol['promedio_enviado'],
            marker_color=COLORS['info'],
            text=df_vol['promedio_enviado'].apply(lambda x: f'{x:.2f} {t("eth")}'),
            textposition='outside'
        ))
        
        fig3.add_trace(go.Bar(
            name=t('max_sent'),
            x=df_vol['tipo'],
            y=df_vol['max_enviado'],
            marker_color=COLORS['primary'],
            text=df_vol['max_enviado'].apply(lambda x: f'{x:.2f} {t("eth")}'),
            textposition='outside'
        ))
        
        fig3.update_layout(
            title=t('comparison'),
            barmode='group',
            height=500,
            yaxis_title=t('eth'),
            xaxis_title=t('account_type'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        col_vol_insight, col_vol_table = st.columns(2)
        
        with col_vol_insight:
            legit_avg = df_vol[df_vol['es_fraude']==0]['promedio_enviado'].values[0]
            fraud_avg = df_vol[df_vol['es_fraude']==1]['promedio_enviado'].values[0]
            
            ratio = (legit_avg/fraud_avg) if fraud_avg > 0 else 0
            
            st.markdown(f"""
            <div style="background: {COLORS['info']}20; padding: 1rem; border-radius: 12px;">
                <h4 style="color: {COLORS['info']};">{t('counterintuitive')}</h4>
                <p style="color: {COLORS['text']};">{t('fraud_move_less')} <strong>{ratio:.0f}x</strong> {t('times_less_eth')}</p>
                <ul style="color: {COLORS['text']};">
                    <li>{t('legit_avg')}: <strong>{legit_avg:.2f} ETH</strong></li>
                    <li>{t('fraud_avg')}: <strong>{fraud_avg:.2f} ETH</strong></li>
                </ul>
                <p style="color: {COLORS['text']};">{t('small_volumes')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_vol_table:
            st.markdown(f"<h4 style='color: {COLORS['text']};'>{t('volume_table')}</h4>", unsafe_allow_html=True)
            vol_display = df_vol[['tipo', 'min_enviado', 'promedio_enviado', 'max_enviado', 'volumen_total_movido']].copy()
            vol_display.columns = [t('type'), t('min_eth'), t('avg_eth'), t('max_eth'), t('total_volume')]
            
            st.dataframe(
                vol_display.style.format({
                    t('min_eth'): '{:.4f}',
                    t('avg_eth'): '{:.2f}',
                    t('max_eth'): '{:.2f}',
                    t('total_volume'): '{:,.0f}'
                }),
                hide_index=True,
                use_container_width=True
            )

# ============================================
# TAB 4: TOKENS SOSPECHOSOS
# ============================================
with tabs[3]:
    st.markdown(f"<h3><span class='gradient-header'>{t('suspicious_tokens')}</span></h3>", unsafe_allow_html=True)
    
    if not df_tokens.empty:
        fig4 = px.bar(
            df_tokens.head(10),
            x='casos_fraude_confirmados',
            y='token_name',
            orientation='h',
            title=t('tokens_highest_fraud'),
            labels={'casos_fraude_confirmados': t('fraud_cases'), 'token_name': t('token')},
            color='casos_fraude_confirmados',
            color_continuous_scale='Reds',
            text='casos_fraude_confirmados'
        )
        
        fig4.update_traces(texttemplate='%{text} ' + t('fraud_cases'), textposition='outside')
        fig4.update_layout(
            height=600,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        
        st.plotly_chart(fig4, use_container_width=True)
        
        col_tok1, col_tok2 = st.columns([2, 1])
        
        with col_tok1:
            st.markdown(f"<h4 style='color: {COLORS['text']};'>{t('token_details')}</h4>", unsafe_allow_html=True)
            tok_display = df_tokens.head(10).copy()
            tok_display['tasa_fraude'] = (tok_display['casos_fraude_confirmados'] / tok_display['menciones'] * 100).round(1)
            tok_display.columns = [t('token'), t('mentions'), t('fraud_cases_count'), t('fraud_rate')]
            st.dataframe(tok_display, hide_index=True, use_container_width=True)
        
        with col_tok2:
            top_token = df_tokens.iloc[0]
            st.markdown(f"""
            <div style="background: {COLORS['warning']}20; padding: 1rem; border-radius: 12px;">
                <h4 style="color: {COLORS['warning']};">{t('most_dangerous')}</h4>
                <p style="font-size: 1.5rem; font-weight: 700; color: {COLORS['warning']};">{top_token['token_name']}</p>
                <ul style="color: {COLORS['text']};">
                    <li>{t('fraud_cases')}: {top_token['casos_fraude_confirmados']}</li>
                    <li>{t('mentions')}: {top_token['menciones']}</li>
                    <li>{t('fraud_rate')}: {(top_token['casos_fraude_confirmados']/top_token['menciones']*100):.1f}%</li>
                </ul>
                <p style="color: {COLORS['text']};"><strong>Action:</strong> {t('action_blacklist')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(t('no_token_data'))

# ============================================
# TAB 5: CUENTAS FANTASMA (CORREGIDO)
# ============================================
with tabs[4]:
    st.markdown(f"<h3><span class='gradient-header'>{t('ghost_accounts')}</span></h3>", unsafe_allow_html=True)
    
    if not df_vulnerabilidad.empty:
        df_vul = df_vulnerabilidad.copy()
        df_vul['tipo'] = df_vul['es_fraude'].map({0: t('legitimate'), 1: t('fraud')})
        
        fig5 = px.pie(
            df_vul,
            values='cuentas_balance_cero',
            names='tipo',
            title=t('zero_balance_dist'),
            color='tipo',
            color_discrete_map={t('legitimate'): COLORS['info'], t('fraud'): COLORS['warning']},
            hole=0.4
        )
        
        fig5.update_traces(textposition='inside', textinfo='percent+label+value')
        fig5.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        
        st.plotly_chart(fig5, use_container_width=True)
        
        ghost_features = t('ghost_features')
        if isinstance(ghost_features, list):
            features_list = ghost_features
        else:
            features_list = ['Disposable accounts (use and discard)', 'Spam bots', 'Honey pots (traps to receive funds)']
        
        features_html = ''.join([f'<li>{f}</li>' for f in features_list])
        
        st.markdown(f"""
        <div style="background: {COLORS['info']}20; padding: 1.5rem; border-radius: 12px;">
            <h4 style="color: {COLORS['info']};">{t('pattern_identified')}</h4>
            <p style="color: {COLORS['text']};">{t('ghost_description')}</p>
            <ul style="color: {COLORS['text']};">{features_html}</ul>
            <p style="color: {COLORS['text']};"><strong>{t('recommendation')}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Mostrar datos de demostración para que se vea algo
        st.info(t('no_vulnerability'))
        
        # Datos de demostración
        st.markdown(f"**{t('demo_data')}**")
        
        demo_data = pd.DataFrame({
            t('type'): [t('legitimate'), t('fraud')],
            'count': [7200, 2641]
        })
        
        fig_demo = px.pie(
            demo_data,
            values='count',
            names=t('type'),
            title=t('zero_balance_dist'),
            color=t('type'),
            color_discrete_map={t('legitimate'): COLORS['info'], t('fraud'): COLORS['warning']},
            hole=0.4
        )
        
        fig_demo.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['text'])
        )
        
        st.plotly_chart(fig_demo, use_container_width=True)

# ============================================
# TAB 6: SISTEMA DE SCORING (CORREGIDO - SIN HTML)
# ============================================
with tabs[5]:
    st.markdown(f"<h3><span class='gradient-header'>{t('scoring_system')}</span></h3>", unsafe_allow_html=True)
    
    # Crear DataFrame para la tabla de factores
    factores_data = {
        t('factor'): [
            t('instant_txs'),
            t('only_sends'),
            t('high_activity'),
            t('extreme_ratio'),
            t('many_contracts')
        ],
        t('weight'): [
            f"3 {t('points')}",
            f"3 {t('points')}",
            f"2 {t('points')}",
            f"2 {t('points')}",
            f"2 {t('points')}"
        ],
        t('criteria'): [
            t('instant_criteria'),
            t('only_sends_criteria'),
            t('high_activity_criteria'),
            t('extreme_ratio_criteria'),
            t('many_contracts_criteria')
        ]
    }
    
    df_factores = pd.DataFrame(factores_data)
    
    st.markdown(f"<h4 style='color: {COLORS['primary']};'>{t('risk_factors')}</h4>", unsafe_allow_html=True)
    st.dataframe(
        df_factores,
        hide_index=True,
        use_container_width=True,
        column_config={
            t('factor'): st.column_config.TextColumn(t('factor')),
            t('weight'): st.column_config.TextColumn(t('weight'), width="small"),
            t('criteria'): st.column_config.TextColumn(t('criteria'), width="large")
        }
    )
    
    st.markdown(f"<h4 style='color: {COLORS['primary']}; margin-top: 2rem;'>{t('risk_classification')}</h4>", unsafe_allow_html=True)
    
    # Usar st.columns para las clasificaciones
    col_risk1, col_risk2, col_risk3, col_risk4 = st.columns(4)
    
    with col_risk1:
        st.markdown(f"""
        <div style="background: {COLORS['warning']}20; padding: 1rem; border-radius: 8px; border: 1px solid {COLORS['border']}; text-align: center;">
            <p style="color: {COLORS['warning']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{t('high_risk')}</p>
            <p style="color: {COLORS['text']}; font-size: 1rem; margin: 0.5rem 0;">≥8 {t('points')}</p>
            <p style="color: {COLORS['text']}; font-size: 0.9rem; margin: 0;">58% {t('fraud_rate_text')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_risk2:
        st.markdown(f"""
        <div style="background: {COLORS['secondary']}20; padding: 1rem; border-radius: 8px; border: 1px solid {COLORS['border']}; text-align: center;">
            <p style="color: {COLORS['secondary']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{t('medium_risk')}</p>
            <p style="color: {COLORS['text']}; font-size: 1rem; margin: 0.5rem 0;">5-7 {t('points')}</p>
            <p style="color: {COLORS['text']}; font-size: 0.9rem; margin: 0;">13% {t('fraud_rate_text')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_risk3:
        st.markdown(f"""
        <div style="background: {COLORS['info']}20; padding: 1rem; border-radius: 8px; border: 1px solid {COLORS['border']}; text-align: center;">
            <p style="color: {COLORS['info']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{t('low_risk')}</p>
            <p style="color: {COLORS['text']}; font-size: 1rem; margin: 0.5rem 0;">2-4 {t('points')}</p>
            <p style="color: {COLORS['text']}; font-size: 0.9rem; margin: 0;">6% {t('fraud_rate_text')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_risk4:
        st.markdown(f"""
        <div style="background: {COLORS['success']}20; padding: 1rem; border-radius: 8px; border: 1px solid {COLORS['border']}; text-align: center;">
            <p style="color: {COLORS['success']}; font-size: 1.2rem; font-weight: 700; margin: 0;">{t('no_risk')}</p>
            <p style="color: {COLORS['text']}; font-size: 1rem; margin: 0.5rem 0;">0-1 {t('points')}</p>
            <p style="color: {COLORS['text']}; font-size: 0.9rem; margin: 0;">7% {t('fraud_rate_text')}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# PLAN DE ACCIÓN
# ============================================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown(f"<h2>🎯 <span class='gradient-header'>{t('action_plan')}</span></h2>", unsafe_allow_html=True)

col_rec1, col_rec2, col_rec3 = st.columns(3)

with col_rec1:
    actions_immediate = t('actions_immediate')
    if isinstance(actions_immediate, list):
        actions_list = actions_immediate
    else:
        actions_list = ['Blacklist top 5 tokens', 'Score ≥8: Auto-block', 'Daily manual review']
    
    actions_html = ''.join([f'<li>{a}</li>' for a in actions_list])
    
    st.markdown(f"""
    <div style="background: {COLORS['warning']}20; padding: 1.5rem; border-radius: 12px;">
        <span class="badge badge-warning" style="font-size: 1rem;">{t('immediate')}</span>
        <h4 style="color: {COLORS['warning']};">{t('this_week')}</h4>
        <ul style="color: {COLORS['text']};">{actions_html}</ul>
    </div>
    """, unsafe_allow_html=True)

with col_rec2:
    actions_short = t('actions_short')
    if isinstance(actions_short, list):
        actions_list = actions_short
    else:
        actions_list = ['Real-time alerts', 'Improve ML model', 'Add new features']
    
    actions_html = ''.join([f'<li>{a}</li>' for a in actions_list])
    
    st.markdown(f"""
    <div style="background: {COLORS['secondary']}20; padding: 1.5rem; border-radius: 12px;">
        <span class="badge badge-info" style="font-size: 1rem;">{t('short_term')}</span>
        <h4 style="color: {COLORS['secondary']};">{t('this_month')}</h4>
        <ul style="color: {COLORS['text']};">{actions_html}</ul>
    </div>
    """, unsafe_allow_html=True)

with col_rec3:
    actions_medium = t('actions_medium')
    if isinstance(actions_medium, list):
        actions_list = actions_medium
    else:
        actions_list = ['Graph network analysis', 'Share blacklists', 'Common database']
    
    actions_html = ''.join([f'<li>{a}</li>' for a in actions_list])
    
    st.markdown(f"""
    <div style="background: {COLORS['info']}20; padding: 1.5rem; border-radius: 12px;">
        <span class="badge badge-success" style="font-size: 1rem;">{t('medium_term')}</span>
        <h4 style="color: {COLORS['info']};">{t('this_quarter')}</h4>
        <ul style="color: {COLORS['text']};">{actions_html}</ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; padding: 2rem;">
    <div style="display: flex; justify-content: center; gap: 0.5rem; margin-bottom: 1rem;">
        <span class="badge badge-primary">Python</span>
        <span class="badge badge-primary">SQL</span>
        <span class="badge badge-primary">Streamlit</span>
        <span class="badge badge-primary">Plotly</span>
        <span class="badge badge-success">{t('style')}</span>
        <span class="badge badge-success">Bilingual</span>
    </div>
    <p style="color: {COLORS['text_secondary']};">Ethereum Fraud Detection · {t('developed_by')}</p>
    <p style="color: {COLORS['text_secondary']};">{datetime.now().strftime('%Y')} · {t('rights')}</p>
</div>
""", unsafe_allow_html=True)