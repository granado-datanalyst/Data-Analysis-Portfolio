import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================
# CONFIGURACIÓN
# ============================================

st.set_page_config(
    page_title="Series del Siglo XXI — Colección del Peri",
    layout="wide",
    page_icon="🎬"
)

# Nombre de la columna de nota en los datos vs cómo la mostramos
COL_PERI_RATE = "Peri Rate"  # nombre para mostrar; en Excel puede ser "Tu Nota" o "Peri Rate"

# Tema: oscuro o claro (naranja y negro en ambos)
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def css_theme(tema):
    if tema == "dark":
        return """
        <style>
        .main, [data-testid="stAppViewContainer"] { background-color: #0d0d0d !important; }
        [data-testid="stHeader"] { background: #0d0d0d !important; }
        [data-testid="stSidebar"] { background-color: #1a1a1a !important; }
        .stMetric { 
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            border: 1px solid #ff8c00;
            color: #ff8c00;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(255,140,0,0.15);
        }
        .metric-label { color: rgba(255,140,0,0.9) !important; }
        .metric-value { color: #ff8c00 !important; font-weight: bold !important; }
        h1, h2, h3, p, label, span { color: #f0f0f0 !important; }
        .stDataFrame { border: 1px solid #333; border-radius: 8px; }
        </style>
        """
    else:
        return """
        <style>
        .main, [data-testid="stAppViewContainer"] { background-color: #fafafa !important; }
        [data-testid="stHeader"] { background: #fafafa !important; }
        [data-testid="stSidebar"] { background-color: #fff5eb !important; }
        .stMetric { 
            background: linear-gradient(135deg, #fff5eb 0%, #ffe4cc 100%);
            border: 1px solid #ff8c00;
            color: #1a1a1a;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(255,140,0,0.2);
        }
        .metric-label { color: #b35c00 !important; }
        .metric-value { color: #1a1a1a !important; font-weight: bold !important; }
        h1, h2, h3, p, label, span { color: #1a1a1a !important; }
        .stDataFrame { border: 1px solid #ff8c00; border-radius: 8px; }
        </style>
        """

st.markdown(css_theme(st.session_state.theme), unsafe_allow_html=True)

# ============================================
# FUNCIONES
# ============================================

@st.cache_data
def cargar_datos():
    """Carga todas las hojas del Excel"""
    try:
        # Hoja 1: Todas las Series
        df_todas = pd.read_excel('TOP SERIES DEL SIGLO XXI.xlsx', sheet_name='Todas las Series')
        
        # Hoja 2: Series Vistas
        df_vistas = pd.read_excel('TOP SERIES DEL SIGLO XXI.xlsx', sheet_name='Series Vistas')
        
        # Hoja 3: Por Década
        df_decadas = pd.read_excel('TOP SERIES DEL SIGLO XXI.xlsx', sheet_name='Por Década')
        
        # Hoja 4: Consenso vs Joyas (necesita limpieza)
        df_consenso_raw = pd.read_excel('TOP SERIES DEL SIGLO XXI.xlsx', sheet_name='Consenso vs Joyas')
        
        # Limpiar Consenso vs Joyas
        # Las primeras filas son Consenso Universal
        idx_joyas = df_consenso_raw[df_consenso_raw.iloc[:, 0].str.contains('JOYAS ESCONDIDAS', na=False)].index
        
        if len(idx_joyas) > 0:
            idx_split = idx_joyas[0]
            
            # Consenso Universal
            df_consenso = df_consenso_raw.iloc[1:idx_split].copy()
            df_consenso.columns = ['Serie', 'Tu Nota', 'IMDb', 'RT%']
            df_consenso = df_consenso[df_consenso['Serie'].notna()]
            
            # Joyas Escondidas
            df_joyas = df_consenso_raw.iloc[idx_split+2:].copy()
            df_joyas.columns = ['Serie', 'Tu Nota', 'IMDb', 'RT%']
            df_joyas = df_joyas[df_joyas['Serie'].notna()]
        else:
            df_consenso = pd.DataFrame()
            df_joyas = pd.DataFrame()
        
        # Hoja 5: Recomendaciones
        df_recomendaciones = pd.read_excel('TOP SERIES DEL SIGLO XXI.xlsx', sheet_name='Recomendaciones Faltantes')
        
        return df_todas, df_vistas, df_decadas, df_consenso, df_joyas, df_recomendaciones
    
    except Exception as e:
        st.error(f"❌ Error cargando datos: {e}")
        return None, None, None, None, None, None

# ============================================
# CARGAR DATOS
# ============================================

df_todas, df_vistas, df_decadas, df_consenso, df_joyas, df_recomendaciones = cargar_datos()

if df_todas is None:
    st.stop()

# Columna de nota: en Excel puede venir como "Tu Nota" o "Peri Rate"
def col_peri_rate(df):
    for c in ["Peri Rate", "Tu Nota", "Peri Rate ", "Tu Nota "]:
        if c.strip() in [x.strip() for x in df.columns]:
            return [x for x in df.columns if x.strip() == c.strip()][0]
    return None

# ============================================
# SIDEBAR - TEMA Y FILTROS
# ============================================

st.sidebar.header("🎨 Tema")
col_oscuro, col_claro = st.sidebar.columns(2)
with col_oscuro:
    if st.button("🌙 **Oscuro**", use_container_width=True):
        st.session_state.theme = "dark"
        st.rerun()
with col_claro:
    if st.button("☀️ **Claro**", use_container_width=True):
        st.session_state.theme = "light"
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros Globales")

# Selector de dataset base
vista_base = st.sidebar.radio(
    "Ver",
    ["Todas", "Solo Vistas", "Pendientes"],
    horizontal=True
)

if vista_base == "Todas":
    df_base = df_todas.copy()
elif vista_base == "Solo Vistas":
    df_base = df_vistas.copy()
else:
    df_base = df_recomendaciones.copy()

# Búsqueda
query = st.sidebar.text_input("🔎 Buscar serie", placeholder="Ej: Breaking Bad")
if query and 'Serie' in df_base.columns:
    df_base = df_base[df_base['Serie'].str.contains(query, case=False, na=False)]

st.sidebar.markdown(f"**Series encontradas:** {len(df_base)}")

# ============================================
# HEADER Y MÉTRICAS
# ============================================

st.title("🎬 Top Series del Siglo XXI — Colección del Peri")
st.markdown("**Colección del Peri:** series vistas, consenso y lo que el Peri va a ver en breve")

st.markdown("### 📊 Resumen de la Colección del Peri")

col1, col2, col3, col4, col5 = st.columns(5)
peri_col = col_peri_rate(df_vistas)

with col1:
    st.metric("📺 Total Series", len(df_todas), help="Series en la colección")

with col2:
    st.metric("✅ Vistas", len(df_vistas), f"{len(df_vistas)/len(df_todas)*100:.0f}%")

with col3:
    if not df_vistas.empty and peri_col:
        promedio = pd.to_numeric(df_vistas[peri_col], errors="coerce").mean()
        st.metric("⭐ Promedio Peri Rate", f"{promedio:.2f}", help="Promedio de calificaciones del Peri")

with col4:
    st.metric("🏆 Consenso", len(df_consenso), help="Series de consenso universal")

with col5:
    st.metric("⏳ Pendientes", len(df_recomendaciones), help="Lo que el Peri va a ver en breve")

# ============================================
# TABS PRINCIPALES
# ============================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visión General",
    "🏆 Rankings",
    "📈 Evolución Temporal",
    "💎 Consenso & Joyas",
    "🎯 Pendientes del Peri",
])

# ============================================
# TAB 1: VISIÓN GENERAL
# ============================================

with tab1:
    st.subheader("📊 Análisis de Calificaciones")
    
    col_v1, col_v2 = st.columns(2)
    
    # Gráfico 1: Distribución Peri Rate
    with col_v1:
        if peri_col and not df_vistas.empty:
            df_plot = df_vistas.copy()
            df_plot[COL_PERI_RATE] = pd.to_numeric(df_plot[peri_col], errors="coerce")
            df_plot = df_plot[df_plot[COL_PERI_RATE].notna()]
            if not df_plot.empty:
                st.markdown("**Distribución del Peri Rate**")
                fig_dist = px.histogram(
                    df_plot,
                    x=COL_PERI_RATE,
                    nbins=20,
                    title="Distribución de calificaciones (Peri Rate)",
                    labels={COL_PERI_RATE: "Peri Rate", "count": "Cantidad"},
                    color_discrete_sequence=["#ff8c00"],
                )
                fig_dist.update_layout(showlegend=False, height=400, template="plotly_white" if st.session_state.theme == "light" else "plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_dist, use_container_width=True)
                notas = df_plot[COL_PERI_RATE]
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    st.metric("Máxima", f"{notas.max():.1f}")
                with col_s2:
                    st.metric("Mediana", f"{notas.median():.1f}")
                with col_s3:
                    st.metric("Desv. Est.", f"{notas.std():.2f}")
    
    # Tabla: IMDb, RT y Peri Rate (las tres líneas de valoración)
    with col_v2:
        cols_tabla = ["Serie"]
        if "IMDb" in df_vistas.columns:
            cols_tabla.append("IMDb")
        if "RT%" in df_vistas.columns:
            cols_tabla.append("RT%")
        if peri_col:
            cols_tabla.append(peri_col)
        cols_tabla = [c for c in cols_tabla if c in df_vistas.columns]
        if len(cols_tabla) >= 2 and not df_vistas.empty:
            st.markdown("**IMDb, Rotten Tomatoes y Peri Rate**")
            tabla_comp = df_vistas[cols_tabla].copy()
            tabla_comp = tabla_comp.rename(columns={peri_col: COL_PERI_RATE}) if peri_col else tabla_comp
            if COL_PERI_RATE in tabla_comp.columns:
                tabla_comp = tabla_comp.dropna(subset=[COL_PERI_RATE])
            tabla_comp = tabla_comp.head(50)
            st.dataframe(tabla_comp, use_container_width=True, hide_index=True, height=400)
    
    # Últimas series agregadas
    st.markdown("---")
    st.markdown("### 🆕 Últimas series agregadas a la colección")
    
    if not df_vistas.empty:
        disp_cols = ["Serie"]
        if peri_col:
            disp_cols.append(peri_col)
        for c in ["IMDb", "RT%", "Año"]:
            if c in df_vistas.columns and c not in disp_cols:
                disp_cols.append(c)
        ultimas = df_vistas.head(10)[disp_cols].copy()
        if peri_col and peri_col != COL_PERI_RATE:
            ultimas = ultimas.rename(columns={peri_col: COL_PERI_RATE})
        st.dataframe(ultimas, use_container_width=True, hide_index=True)

# ============================================
# TAB 2: RANKINGS
# ============================================

with tab2:
    st.subheader("🏆 Rankings y Tops")
    
    col_r1, col_r2 = st.columns(2)
    
    # Top 20 por Peri Rate
    with col_r1:
        st.markdown("**🥇 Top 20 por Peri Rate**")
        
        if peri_col and not df_vistas.empty:
            df_sort = df_vistas.copy()
            df_sort["_peri_num"] = pd.to_numeric(df_sort[peri_col], errors="coerce")
            top20 = df_sort.dropna(subset=["_peri_num"]).nlargest(20, "_peri_num")
            top20 = top20[["Serie", peri_col] + [c for c in ["IMDb", "RT%"] if c in top20.columns]].copy()
            top20 = top20.rename(columns={peri_col: COL_PERI_RATE})
            if not top20.empty:
                fig_top = px.bar(
                    top20.sort_values(COL_PERI_RATE),
                    x=COL_PERI_RATE,
                    y="Serie",
                    orientation="h",
                    title="Favoritas del Peri (Peri Rate)",
                    labels={COL_PERI_RATE: "Peri Rate", "Serie": ""},
                    color=COL_PERI_RATE,
                    color_continuous_scale=["#1a1a1a", "#ff8c00"],
                )
                fig_top.update_layout(showlegend=False, height=700)
                st.plotly_chart(fig_top, use_container_width=True)
    
    # Top por IMDb
    with col_r2:
        st.markdown("**🎬 Top 20 por IMDb**")
        
        if "IMDb" in df_vistas.columns and not df_vistas.empty:
            top_imdb = df_vistas.nlargest(20, "IMDb")[["Serie", "IMDb"] + ([peri_col] if peri_col else []) + (["RT%"] if "RT%" in df_vistas.columns else [])].copy()
            if peri_col and peri_col in top_imdb.columns:
                top_imdb = top_imdb.rename(columns={peri_col: COL_PERI_RATE})
            fig_imdb = px.bar(
                top_imdb.sort_values("IMDb"),
                x="IMDb",
                y="Serie",
                orientation="h",
                title="Mejor valoradas en IMDb",
                labels={"IMDb": "IMDb Rating", "Serie": ""},
                color="IMDb",
                color_continuous_scale=["#1a1a1a", "#ff8c00"],
            )
            fig_imdb.update_layout(showlegend=False, height=700)
            st.plotly_chart(fig_imdb, use_container_width=True)
    
    # Top por RT
    st.markdown("---")
    st.markdown("### 🍅 Top 15 por Rotten Tomatoes")
    
    if "RT%" in df_vistas.columns and not df_vistas.empty:
        top_rt = df_vistas.nlargest(15, "RT%")[["Serie", "RT%"] + ([peri_col] if peri_col else []) + (["IMDb"] if "IMDb" in df_vistas.columns else [])].copy()
        if peri_col and peri_col in top_rt.columns:
            top_rt = top_rt.rename(columns={peri_col: COL_PERI_RATE})
        fig_rt = px.bar(
            top_rt,
            x="Serie",
            y="RT%",
            title="Favoritas de la crítica (RT)",
            labels={"RT%": "Rotten Tomatoes %"},
            color="RT%",
            color_continuous_scale=["#1a1a1a", "#ff6600"],
        )
        fig_rt.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_rt, use_container_width=True)

# ============================================
# TAB 3: EVOLUCIÓN TEMPORAL
# ============================================

with tab3:
    st.subheader("📈 Evolución por Década")
    
    if not df_decadas.empty:
        st.markdown("**Tendencia de calidad a lo largo del tiempo**")
        
        fig_decadas = go.Figure()
        
        # Promedio Peri Rate (columna en Excel puede ser "Tu Promedio")
        col_promedio_peri = "Tu Promedio" if "Tu Promedio" in df_decadas.columns else None
        if col_promedio_peri:
            fig_decadas.add_trace(go.Scatter(
                x=df_decadas["Década"],
                y=df_decadas[col_promedio_peri],
                mode="lines+markers",
                name="Promedio Peri Rate",
                line=dict(color="#ff8c00", width=3),
                marker=dict(size=12),
            ))
        
        # IMDb promedio
        fig_decadas.add_trace(go.Scatter(
            x=df_decadas["Década"],
            y=df_decadas["IMDb Promedio"],
            mode="lines+markers",
            name="IMDb Promedio",
            line=dict(color="#ff6600", width=3),
            marker=dict(size=12),
        ))
        
        # RT promedio
        if "RT% Promedio" in df_decadas.columns:
            fig_decadas.add_trace(go.Scatter(
                x=df_decadas["Década"],
                y=df_decadas["RT% Promedio"] / 10,
                mode="lines+markers",
                name="RT Promedio (/10)",
                line=dict(color="#cc5200", width=3),
                marker=dict(size=12),
            ))
        
        fig_decadas.update_layout(
            title="Evolución de calificaciones por década",
            xaxis_title="Década",
            yaxis_title="Calificación promedio",
            hovermode="x unified",
            height=500,
        )
        
        st.plotly_chart(fig_decadas, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📋 Resumen por Década")
        
        st.dataframe(df_decadas, use_container_width=True, hide_index=True)
        
        if col_promedio_peri:
            mejor_decada = df_decadas.loc[df_decadas[col_promedio_peri].idxmax()]
            st.success(f"🏆 **Mejor década (Peri Rate):** {mejor_decada['Década']} (promedio: {mejor_decada[col_promedio_peri]:.2f})")
        if "Series Vistas" in df_decadas.columns:
            mas_series = df_decadas.loc[df_decadas["Series Vistas"].idxmax()]
            st.info(f"📺 **Década con más series vistas:** {mas_series['Década']} ({int(mas_series['Series Vistas'])} series)")

# ============================================
# TAB 4: CONSENSO & JOYAS
# ============================================

with tab4:
    st.subheader("💎 Consenso Universal vs Joyas Escondidas")
    
    col_c1, col_c2 = st.columns(2)
    
    # En Consenso/Joyas el Excel se parsea con columna 'Tu Nota' → mostramos como Peri Rate
    consenso_col = "Tu Nota" if "Tu Nota" in (df_consenso.columns if not df_consenso.empty else []) else None
    
    with col_c1:
        st.markdown("### 🏆 Consenso Universal")
        st.markdown("*RT≥90, IMDb≥8.0, Peri Rate≥9.0*")
        
        if not df_consenso.empty:
            st.markdown(f"**{len(df_consenso)} series de consenso**")
            consenso_display = df_consenso.copy()
            if consenso_col:
                consenso_display = consenso_display.rename(columns={consenso_col: COL_PERI_RATE})
                consenso_display = consenso_display.sort_values(COL_PERI_RATE, ascending=False)
            else:
                consenso_display = consenso_display.sort_values(consenso_display.columns[1], ascending=False)
            
            st.dataframe(consenso_display, use_container_width=True, hide_index=True, height=600)
            
            if len(consenso_display) > 0 and COL_PERI_RATE in consenso_display.columns:
                top_consenso = consenso_display.head(10)
                fig_consenso = px.bar(
                    top_consenso.sort_values(COL_PERI_RATE),
                    x=COL_PERI_RATE,
                    y="Serie",
                    orientation="h",
                    title="Top 10 Consenso Universal",
                    color=COL_PERI_RATE,
                    color_continuous_scale=["#1a1a1a", "#ff8c00"],
                )
                fig_consenso.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig_consenso, use_container_width=True)
    
    with col_c2:
        st.markdown("### 💎 Joyas Escondidas")
        st.markdown("*IMDb<7.8, Peri Rate≥8.5*")
        
        if not df_joyas.empty:
            st.markdown(f"**{len(df_joyas)} joyas infravaloradas**")
            joyas_display = df_joyas.copy()
            if consenso_col:
                joyas_display = joyas_display.rename(columns={consenso_col: COL_PERI_RATE})
                joyas_display = joyas_display.sort_values(COL_PERI_RATE, ascending=False)
            else:
                joyas_display = joyas_display.sort_values(joyas_display.columns[1], ascending=False)
            
            st.dataframe(joyas_display, use_container_width=True, hide_index=True, height=600)
            
            if len(joyas_display) > 0 and COL_PERI_RATE in joyas_display.columns:
                top_joyas = joyas_display.head(10)
                fig_joyas = px.bar(
                    top_joyas.sort_values(COL_PERI_RATE),
                    x=COL_PERI_RATE,
                    y="Serie",
                    orientation="h",
                    title="Top 10 Joyas Escondidas",
                    color=COL_PERI_RATE,
                    color_continuous_scale=["#1a1a1a", "#ff6600"],
                )
                fig_joyas.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig_joyas, use_container_width=True)

# ============================================
# TAB 5: PENDIENTES DEL PERI (LO QUE VA A VER EN BREVE)
# ============================================

with tab5:
    st.subheader("🎯 Pendientes del Peri — Lo que voy a ver en breve")
    
    if not df_recomendaciones.empty:
        st.markdown(f"**{len(df_recomendaciones)} series que el Peri tiene pendientes, ordenadas por score**")
        
        col_f1, col_f2 = st.columns([3, 1])
        
        with col_f1:
            min_score = st.slider(
                "Score mínimo",
                float(df_recomendaciones["Score Promedio"].min()),
                float(df_recomendaciones["Score Promedio"].max()),
                8.0,
                0.1,
            )
        
        with col_f2:
            cantidad = st.selectbox("Mostrar top", [10, 20, 50, 100], index=1)
        
        df_rec_filtrado = df_recomendaciones[df_recomendaciones["Score Promedio"] >= min_score]
        df_rec_top = df_rec_filtrado.head(cantidad).copy()
        
        def categorizar_score(score):
            if score >= 9.0:
                return "🔥 Imperdibles"
            elif score >= 8.5:
                return "⭐ Excelentes"
            elif score >= 8.0:
                return "👍 Muy Buenas"
            else:
                return "✅ Buenas"
        
        df_rec_top["Categoría"] = df_rec_top["Score Promedio"].apply(categorizar_score)
        
        col_r1, col_r2 = st.columns([2, 1])
        
        with col_r1:
            st.markdown(f"**Top {len(df_rec_top)} pendientes del Peri**")
            
            fig_rec = px.bar(
                df_rec_top.head(20).sort_values("Score Promedio"),
                x="Score Promedio",
                y="Serie",
                orientation="h",
                title="Top 20 pendientes por score",
                labels={"Score Promedio": "Score (RT + IMDb) / 2"},
                color="Score Promedio",
                color_continuous_scale=["#1a1a1a", "#ff8c00"],
            )
            fig_rec.update_layout(showlegend=False, height=700)
            st.plotly_chart(fig_rec, use_container_width=True)
        
        with col_r2:
            st.markdown("**Por categoría**")
            categoria_counts = df_rec_top["Categoría"].value_counts()
            fig_cat = px.pie(
                values=categoria_counts.values,
                names=categoria_counts.index,
                title="Pendientes por calidad",
                color_discrete_sequence=["#ff8c00", "#ff6600", "#cc5200", "#1a1a1a"],
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📋 Lista de pendientes del Peri")
        
        cols_tabla = ["Serie", "Score Promedio", "IMDb", "Categoría"]
        if "RT (/10)" in df_rec_top.columns:
            cols_tabla.insert(3, "RT (/10)")
        cols_tabla = [c for c in cols_tabla if c in df_rec_top.columns]
        st.dataframe(df_rec_top[cols_tabla], use_container_width=True, hide_index=True, height=500)
        
        csv = df_rec_top.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Descargar pendientes (CSV)",
            data=csv,
            file_name=f"pendientes_peri_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("**Colección del Peri** — Dashboard de series del Siglo XXI")