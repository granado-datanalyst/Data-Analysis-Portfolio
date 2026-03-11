import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# CONFIGURACIÓN
# ============================================

st.set_page_config(
    page_title="La Liga Pro Scouting",
    layout="wide",
    page_icon="⚽"
)

# CSS personalizado
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)


# ============================================
# FUNCIONES
# ============================================

@st.cache_data
def cargar_y_unir_datos():
    """Carga y unifica las 3 hojas del Excel"""
    # Usamos os para encontrar el archivo en la nube
    directorio_actual = os.path.dirname(__file__)
    archivo = os.path.join(directorio_actual, 'sofascore top 200 main stats.xlsx')

    try:
        atq = pd.read_excel(archivo, sheet_name='player la liga attack stats')
        dfe = pd.read_excel(archivo, sheet_name='player la liga deffensive stats')
        pas = pd.read_excel(archivo, sheet_name='player la liga passing stats')

        # Unir datasets
        df = pd.merge(atq, dfe.drop(columns=['#'], errors='ignore'), on='Name', how='outer')
        df = pd.merge(df, pas.drop(columns=['#'], errors='ignore'), on='Name', how='outer')

        # Limpieza de números básica
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='ignore')
                except Exception:
                    pass

        # Rellenar NaN con 0 para métricas numéricas
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        return df

    except Exception as e:
        st.error(f"❌ Error cargando datos: {e}")
        return pd.DataFrame()


def first_existing_column(df: pd.DataFrame, candidates) -> str | None:
    """Devuelve la primera columna existente de una lista de candidatos."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


# ============================================
# INTERFAZ PRINCIPAL
# ============================================

st.title("⚽ La Liga Pro Scouting Dashboard")
st.markdown("**Análisis completo:** Ataque + Defensa + Pase")

# Cargar datos
df = cargar_y_unir_datos()

if df.empty:
    st.stop()

# ============================================
# SIDEBAR - FILTROS (Equipo / Posición / Nombre)
# ============================================

st.sidebar.header("🔍 Filtros")

query = st.sidebar.text_input("Buscar jugador", placeholder="Ej: Lewandowski")

df_filtrado = df.copy()

if 'Team' in df.columns:
    equipos = sorted(df['Team'].dropna().unique())
    equipos_sel = st.sidebar.multiselect("Equipo", equipos)
    if equipos_sel:
        df_filtrado = df_filtrado[df_filtrado['Team'].isin(equipos_sel)]

if 'Position' in df.columns:
    posiciones = sorted(df['Position'].dropna().unique())
    pos_sel = st.sidebar.multiselect("Posición", posiciones)
    if pos_sel:
        df_filtrado = df_filtrado[df_filtrado['Position'].isin(pos_sel)]

if query and 'Name' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Name'].str.contains(query, case=False, na=False)]

st.sidebar.markdown(f"**Jugadores encontrados:** {len(df_filtrado)}")


# ============================================
# MÉTRICAS PRINCIPALES (HEADER)
# ============================================

st.subheader("📊 Métricas principales de La Liga")

col1, col2, col3, col4 = st.columns(4)

# Líder de goles
if 'Goals' in df.columns:
    top_goles = df.nlargest(1, 'Goals')
    if not top_goles.empty:
        col1.metric(
            "👑 Máximo Goleador",
            top_goles['Name'].values[0],
            f"{int(top_goles['Goals'].values[0])} Goles"
        )

# Líder de tackles (debería ser Aramburu)
if 'Tackles' in df.columns:
    top_tackles = df.nlargest(1, 'Tackles')
    if not top_tackles.empty:
        col2.metric(
            "🛡️ Más Tackles",
            top_tackles['Name'].values[0],
            f"{int(top_tackles['Tackles'].values[0])} Tackles"
        )

# Líder de asistencias
if 'Assists' in df.columns:
    top_asistencias = df.nlargest(1, 'Assists')
    if not top_asistencias.empty:
        col3.metric(
            "🎯 Máximo Asistidor",
            top_asistencias['Name'].values[0],
            f"{int(top_asistencias['Assists'].values[0])} Asistencias"
        )

# Mejor pasador (precisión)
if 'Accurate passes %' in df.columns:
    top_precision = df.nlargest(1, 'Accurate passes %')
    if not top_precision.empty:
        col4.metric(
            "📈 Mejor Precisión de Pase",
            top_precision['Name'].values[0],
            f"{top_precision['Accurate passes %'].values[0]:.1f}%"
        )


# ============================================
# TABS DE ANÁLISIS
# ============================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Análisis Ofensivo",
    "🛡️ Análisis Defensivo",
    "📡 Análisis de Pases",
    "🔬 Comparador",
    "📋 Datos Completos"
])


# --- TAB 1: OFENSIVO ---
with tab1:
    st.subheader("Goles vs Asistencias (GA ≥ 10)")

    if not df_filtrado.empty and 'Goals' in df_filtrado.columns and 'Assists' in df_filtrado.columns:
        df_scatter = df_filtrado.copy()
        df_scatter['GA'] = df_scatter['Goals'] + df_scatter['Assists']
        df_scatter = df_scatter[df_scatter['GA'] >= 10]

        if not df_scatter.empty:
            fig1 = px.scatter(
                df_scatter,
                x='Goals',
                y='Assists',
                hover_name='Name',
                size='Total shots' if 'Total shots' in df_scatter.columns else None,
                color='GA',
                color_continuous_scale='RdYlGn',
                title="Relación entre Goles y Asistencias (solo jugadores con ≥ 10 GA)",
                labels={
                    'Goals': 'Goles',
                    'Assists': 'Asistencias',
                    'GA': 'Goles + Asistencias'
                }
            )

            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No hay jugadores con Goles + Asistencias (GA) ≥ 10 bajo los filtros actuales.")
    else:
        st.info("No hay datos suficientes para mostrar el gráfico de Goles vs Asistencias.")

    # Tablas ofensivas
    col_a, col_b = st.columns(2)

    with col_a:
        if 'Goals' in df_filtrado.columns:
            st.markdown("**Top 10 Goleadores**")
            columnas_goles = ['Name', 'Team', 'Position', 'Goals', 'Assists']
            columnas_goles = [c for c in columnas_goles if c in df_filtrado.columns]
            top10_goles = df_filtrado.nlargest(10, 'Goals')[columnas_goles].copy()
            st.dataframe(top10_goles, hide_index=True, use_container_width=True)
        else:
            st.info("No se encontró la columna 'Goals'.")

    with col_b:
        if 'Assists' in df_filtrado.columns:
            st.markdown("**Top 10 Asistidores**")
            columnas_ast = ['Name', 'Team', 'Position', 'Assists', 'Goals']
            columnas_ast = [c for c in columnas_ast if c in df_filtrado.columns]
            top10_ast = df_filtrado.nlargest(10, 'Assists')[columnas_ast].copy()
            st.dataframe(top10_ast, hide_index=True, use_container_width=True)
        else:
            st.info("No se encontró la columna 'Assists'.")

    col_c, col_d = st.columns(2)

    # Top 10 Dribbles (Regates) - usando columna exacta 'Succ. dribbles'
    with col_c:
        if 'Succ. dribbles' in df_filtrado.columns:
            st.markdown("**Top 10 en Dribbles (Succ. dribbles)**")
            columnas_drib = ['Name', 'Team', 'Position', 'Succ. dribbles']
            columnas_drib = [c for c in columnas_drib if c in df_filtrado.columns]
            top10_drib = df_filtrado.nlargest(10, 'Succ. dribbles')[columnas_drib].copy()
            st.dataframe(top10_drib, hide_index=True, use_container_width=True)
        else:
            st.info("No se encontró la columna 'Succ. dribbles' en el dataset.")

    # Top 10 Chances Creadas (usando exactamente 'Big chances created')
    with col_d:
        if 'Big chances created' in df_filtrado.columns:
            st.markdown("**Top 10 en Big chances created**")
            columnas_ch = ['Name', 'Team', 'Position', 'Big chances created']
            columnas_ch = [c for c in columnas_ch if c in df_filtrado.columns]
            top10_ch = df_filtrado.nlargest(10, 'Big chances created')[columnas_ch].copy()
            st.dataframe(top10_ch, hide_index=True, use_container_width=True)
        else:
            st.info("No se encontró la columna 'Big chances created' en el dataset.")


# --- TAB 2: DEFENSIVO ---
with tab2:
    st.subheader("Perfil Defensivo")

    if df_filtrado.empty:
        st.info("No hay datos tras los filtros actuales.")
    else:
        df_def = df_filtrado.copy()

        if 'Tackles' in df_def.columns and 'Blocked shots' in df_def.columns:
            # Cálculo de suma defensiva
            df_def['Suma defensiva'] = df_def['Tackles'] + df_def['Blocked shots']

            # Top 20 por suma defensiva (mismo subconjunto para tabla y scatter)
            df_def_ordenado = df_def.sort_values('Suma defensiva', ascending=False).head(20)

            # Scatter Tackles vs Blocked shots (solo Top 20)
            st.markdown("**Tackles vs Tiros Bloqueados (Top 20 Suma Defensiva)**")
            fig_def = px.scatter(
                df_def_ordenado,
                x='Tackles',
                y='Blocked shots',
                hover_name='Name',
                size='Suma defensiva',
                color='Suma defensiva',
                color_continuous_scale='Blues',
                labels={
                    'Tackles': 'Tackles',
                    'Blocked shots': 'Tiros Bloqueados',
                    'Suma defensiva': 'Tackles + Tiros Bloqueados'
                },
                title="Relación entre Tackles y Tiros Bloqueados (Top 20)"
            )
            st.plotly_chart(fig_def, use_container_width=True)

            st.markdown("**Top 20 por Suma Defensiva (Tackles + Tiros Bloqueados)**")
            columnas_def = ['Name', 'Team', 'Position', 'Tackles', 'Blocked shots', 'Suma defensiva']
            columnas_def = [c for c in columnas_def if c in df_def_ordenado.columns]
            st.dataframe(df_def_ordenado[columnas_def], hide_index=True, use_container_width=True)
        else:
            st.info("No se pueden calcular 'Suma Defensiva' (faltan columnas 'Tackles' o 'Blocked shots').")

        st.markdown("---")
        st.markdown("**Rankings Defensivos Top 10**")

        col1_def, col2_def, col3_def = st.columns(3)

        # Top 10 Tackles
        with col1_def:
            if 'Tackles' in df_def.columns:
                st.markdown("**Top 10 en Tackles**")
                cols = ['Name', 'Team', 'Position', 'Tackles']
                cols = [c for c in cols if c in df_def.columns]
                top10_tackles = df_def.nlargest(10, 'Tackles')[cols].copy()
                st.dataframe(top10_tackles, hide_index=True, use_container_width=True, height=280)
            else:
                st.info("No se encontró la columna 'Tackles'.")

        # Top 10 Interceptions
        with col2_def:
            if 'Interceptions' in df_def.columns:
                st.markdown("**Top 10 en Interceptions**")
                cols = ['Name', 'Team', 'Position', 'Interceptions']
                cols = [c for c in cols if c in df_def.columns]
                top10_inter = df_def.nlargest(10, 'Interceptions')[cols].copy()
                st.dataframe(top10_inter, hide_index=True, use_container_width=True, height=280)
            else:
                st.info("No se encontró la columna 'Interceptions'.")

        # Top 10 Tiros Bloqueados
        with col3_def:
            if 'Blocked shots' in df_def.columns:
                st.markdown("**Top 10 en Tiros Bloqueados**")
                cols = ['Name', 'Team', 'Position', 'Blocked shots']
                cols = [c for c in cols if c in df_def.columns]
                top10_blocked = df_def.nlargest(10, 'Blocked shots')[cols].copy()
                st.dataframe(top10_blocked, hide_index=True, use_container_width=True, height=280)
            else:
                st.info("No se encontró la columna 'Blocked shots'.")


# --- TAB 3: ANÁLISIS DE PASES ---
with tab3:
    st.subheader("Análisis de Pases")

    if df_filtrado.empty:
        st.info("No hay datos tras los filtros actuales.")
    else:
        df_pass = df_filtrado.copy()

        # Métrica combinada de creación: Big chances created + Key passes
        if 'Big chances created' in df_pass.columns and 'Key passes' in df_pass.columns:
            df_pass['Suma creativa'] = df_pass['Big chances created'] + df_pass['Key passes']

            # Top 20 por suma creativa (mismo subconjunto para scatter y tabla)
            df_pass_top20 = df_pass.sort_values('Suma creativa', ascending=False).head(20)

            # Scatter Big chances created vs Key passes (solo Top 20)
            st.markdown("**Big chances created vs Key passes (Top 20 Suma creativa)**")
            fig_pass = px.scatter(
                df_pass_top20,
                x='Key passes',
                y='Big chances created',
                hover_name='Name',
                size='Suma creativa',
                color='Suma creativa',
                color_continuous_scale='RdYlGn',
                labels={
                    'Key passes': 'Key passes',
                    'Big chances created': 'Big chances created',
                    'Suma creativa': 'Big chances created + Key passes'
                },
                title="Relación entre Big chances created y Key passes (Top 20)"
            )
            st.plotly_chart(fig_pass, use_container_width=True)

            # Tabla Top 20 por suma creativa
            st.markdown("**Top 20 por Big chances created + Key passes**")
            cols_top20 = ['Name', 'Team', 'Position', 'Big chances created', 'Key passes', 'Suma creativa']
            cols_top20 = [c for c in cols_top20 if c in df_pass_top20.columns]
            top20_creativo = df_pass_top20[cols_top20].copy()
            st.dataframe(top20_creativo, hide_index=True, use_container_width=True)
        else:
            st.info("No se encontraron ambas columnas 'Big chances created' y 'Key passes'.")

        st.markdown("---")

        col_p1, col_p2, col_p3 = st.columns(3)

        # Top 10 Big chances created
        with col_p1:
            if 'Big chances created' in df_pass.columns:
                st.markdown("**Top 10 Big chances created**")
                cols = ['Name', 'Team', 'Position', 'Big chances created']
                cols = [c for c in cols if c in df_pass.columns]
                top10_big = df_pass.nlargest(10, 'Big chances created')[cols].copy()
                st.dataframe(top10_big, hide_index=True, use_container_width=True, height=280)
            else:
                st.info("No se encontró la columna 'Big chances created'.")

        # Top 10 Accurate passes
        with col_p2:
            if 'Accurate passes' in df_pass.columns:
                st.markdown("**Top 10 Accurate passes**")
                cols = ['Name', 'Team', 'Position', 'Accurate passes']
                cols = [c for c in cols if c in df_pass.columns]
                top10_acc = df_pass.nlargest(10, 'Accurate passes')[cols].copy()
                st.dataframe(top10_acc, hide_index=True, use_container_width=True, height=280)
            else:
                st.info("No se encontró la columna 'Accurate passes'.")

        # Top 10 Key passes
        with col_p3:
            if 'Key passes' in df_pass.columns:
                st.markdown("**Top 10 Key passes**")
                cols = ['Name', 'Team', 'Position', 'Key passes']
                cols = [c for c in cols if c in df_pass.columns]
                top10_key = df_pass.nlargest(10, 'Key passes')[cols].copy()
                st.dataframe(top10_key, hide_index=True, use_container_width=True, height=280)
            else:
                st.info("No se encontró la columna 'Key passes'.")


# --- TAB 4: COMPARADOR ---
with tab4:
    st.subheader("🔬 Comparador Profesional de Jugadores")

    if df_filtrado.empty or 'Name' not in df_filtrado.columns:
        st.info("No hay jugadores disponibles bajo los filtros actuales para comparar.")
    else:
        # Selector de modo
        modo = st.radio(
            "Modo de comparación",
            ["⚡ Rápido (2 jugadores)", "📊 Detallado (hasta 4 jugadores)"],
            horizontal=True
        )

        max_jugadores = 2 if modo == "⚡ Rápido (2 jugadores)" else 4

        # Selector de jugadores (sobre df_filtrado para respetar filtros)
        st.markdown("### Seleccionar jugadores a comparar")

        cols_seleccion = st.columns(max_jugadores)
        jugadores_seleccionados = []

        opciones_jugadores = [''] + sorted(df_filtrado['Name'].dropna().unique().tolist())

        for i, col in enumerate(cols_seleccion):
            with col:
                jugador = st.selectbox(
                    f"Jugador {i+1}",
                    options=opciones_jugadores,
                    key=f'jugador_comp_{i}'
                )
                if jugador:
                    jugadores_seleccionados.append(jugador)

        if len(jugadores_seleccionados) < 2:
            st.info("ℹ️ Selecciona al menos 2 jugadores para comparar.")
        else:
            # Filtrar datos de jugadores seleccionados
            df_comparacion = df_filtrado[df_filtrado['Name'].isin(jugadores_seleccionados)].copy()

            if df_comparacion.empty:
                st.error("❌ No se encontraron datos para los jugadores seleccionados.")
            else:
                # ============================================
                # VISTA GENERAL - CARDS
                # ============================================

                st.markdown("---")
                st.markdown("### 📊 Vista General")

                cols_cards = st.columns(len(jugadores_seleccionados))

                for col, jugador in zip(cols_cards, jugadores_seleccionados):
                    fila = df_comparacion[df_comparacion['Name'] == jugador].head(1)
                    if fila.empty:
                        continue
                    data = fila.iloc[0]

                    with col:
                        st.markdown(f"""
                            <div style='
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 20px;
                                border-radius: 10px;
                                color: white;
                                text-align: center;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            '>
                                <h3 style='margin: 0; font-size: 1.1rem;'>{jugador}</h3>
                                <p style='margin: 5px 0; opacity: 0.9; font-size: 0.85rem;'>
                                    {data.get('Team', 'N/A')} | {data.get('Position', 'N/A')}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        col_m1, col_m2 = st.columns(2)

                        with col_m1:
                            if 'Goals' in data.index:
                                st.metric("⚽ Goles", int(data['Goals']))
                            if 'Tackles' in data.index:
                                st.metric("🛡️ Tackles", int(data['Tackles']))

                        with col_m2:
                            if 'Assists' in data.index:
                                st.metric("🎯 Asist.", int(data['Assists']))
                            if 'Accurate passes %' in data.index:
                                st.metric("📈 Prec.", f"{data['Accurate passes %']:.1f}%")

                # ============================================
                # COMPARACIÓN POR CATEGORÍAS
                # ============================================

                st.markdown("---")
                st.markdown("### 📈 Comparación Detallada")

                tab_of, tab_df, tab_ps = st.tabs(["⚽ Ofensiva", "🛡️ Defensiva", "📡 Pases"])

                # --- OFENSIVA ---
                with tab_of:
                    metricas_ofensivas = {
                        'Goals': '⚽ Goles',
                        'Assists': '🎯 Asistencias',
                        'Total shots': '🎯 Tiros Totales',
                        'Expected goals (xG)': '📊 xG',
                        'Goal conversion %': '💯 Conversión %',
                        'Succ. dribbles': '🏃 Regates',
                        'Big chances missed': '❌ Chances Falladas'
                    }

                    datos_tabla = []
                    for metrica, nombre in metricas_ofensivas.items():
                        if metrica in df_comparacion.columns:
                            fila_met = {'Métrica': nombre}
                            for jugador in jugadores_seleccionados:
                                fila_j = df_comparacion[df_comparacion['Name'] == jugador].head(1)
                                if fila_j.empty:
                                    fila_met[jugador] = '-'
                                    continue
                                valor = fila_j[metrica].values[0]
                                if pd.notna(valor):
                                    if metrica == 'Goal conversion %':
                                        fila_met[jugador] = f"{valor:.1f}%"
                                    elif metrica == 'Expected goals (xG)':
                                        fila_met[jugador] = f"{valor:.2f}"
                                    else:
                                        fila_met[jugador] = int(valor)
                                else:
                                    fila_met[jugador] = '-'
                            datos_tabla.append(fila_met)

                    if datos_tabla:
                        df_tabla_of = pd.DataFrame(datos_tabla)
                        st.dataframe(
                            df_tabla_of,
                            use_container_width=True,
                            hide_index=True,
                            height=300
                        )

                        st.markdown("**Visualización Comparativa**")

                        metricas_graf = ['Goals', 'Assists', 'Total shots']
                        metricas_disponibles = [m for m in metricas_graf if m in df_comparacion.columns]

                        if metricas_disponibles:
                            df_plot = df_comparacion[['Name'] + metricas_disponibles].copy()
                            fig_of = px.bar(
                                df_plot.melt(id_vars='Name', value_vars=metricas_disponibles,
                                             var_name='Métrica', value_name='Valor'),
                                x='Name',
                                y='Valor',
                                color='Métrica',
                                barmode='group',
                                title="Comparación de Stats Ofensivas",
                                labels={'Name': 'Jugador', 'Valor': 'Cantidad', 'Métrica': 'Métrica'},
                            )
                            st.plotly_chart(fig_of, use_container_width=True)

                # --- DEFENSIVA ---
                with tab_df:
                    metricas_defensivas = {
                        'Tackles': '⚔️ Tackles',
                        'Interceptions': '🛡️ Intercepciones',
                        'Clearances': '🚫 Despejes',
                        'Blocked shots': '🧱 Tiros Bloqueados',
                        'Errors leading to goal': '⚠️ Errores → Gol'
                    }

                    datos_tabla_def = []
                    for metrica, nombre in metricas_defensivas.items():
                        if metrica in df_comparacion.columns:
                            fila_met = {'Métrica': nombre}
                            for jugador in jugadores_seleccionados:
                                fila_j = df_comparacion[df_comparacion['Name'] == jugador].head(1)
                                if fila_j.empty:
                                    fila_met[jugador] = '-'
                                    continue
                                valor = fila_j[metrica].values[0]
                                fila_met[jugador] = int(valor) if pd.notna(valor) else '-'
                            datos_tabla_def.append(fila_met)

                    if datos_tabla_def:
                        df_tabla_def = pd.DataFrame(datos_tabla_def)
                        st.dataframe(
                            df_tabla_def,
                            use_container_width=True,
                            hide_index=True,
                            height=250
                        )

                        st.markdown("**Perfil Defensivo (Radar)**")

                        metricas_radar = ['Tackles', 'Interceptions', 'Clearances', 'Blocked shots']
                        metricas_disp = [m for m in metricas_radar if m in df_comparacion.columns]

                        if len(metricas_disp) >= 3:
                            import plotly.graph_objects as go

                            fig_radar = go.Figure()
                            colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

                            max_val = max(df_comparacion[m].max() for m in metricas_disp)

                            for idx, jugador in enumerate(jugadores_seleccionados):
                                fila_j = df_comparacion[df_comparacion['Name'] == jugador].head(1)
                                if fila_j.empty:
                                    continue
                                data_jugador = fila_j.iloc[0]
                                valores = [
                                    float(data_jugador[m]) if pd.notna(data_jugador[m]) else 0
                                    for m in metricas_disp
                                ]

                                fig_radar.add_trace(go.Scatterpolar(
                                    r=valores,
                                    theta=metricas_disp,
                                    fill='toself',
                                    name=jugador,
                                    line_color=colores[idx % len(colores)]
                                ))

                            fig_radar.update_layout(
                                polar=dict(radialaxis=dict(visible=True, range=[0, max_val])),
                                showlegend=True,
                                height=500
                            )

                            st.plotly_chart(fig_radar, use_container_width=True)

                # --- PASES ---
                with tab_ps:
                    metricas_pases = {
                        'Assists': '🎯 Asistencias',
                        'Big chances created': '⭐ Chances Creadas',
                        'Key passes': '🔑 Pases Clave',
                        'Accurate passes': '✅ Pases Precisos',
                        'Accurate passes %': '📊 Precisión %'
                    }

                    datos_tabla_pas = []
                    for metrica, nombre in metricas_pases.items():
                        if metrica in df_comparacion.columns:
                            fila_met = {'Métrica': nombre}
                            for jugador in jugadores_seleccionados:
                                fila_j = df_comparacion[df_comparacion['Name'] == jugador].head(1)
                                if fila_j.empty:
                                    fila_met[jugador] = '-'
                                    continue
                                valor = fila_j[metrica].values[0]
                                if pd.notna(valor):
                                    if metrica == 'Accurate passes %':
                                        fila_met[jugador] = f"{valor:.1f}%"
                                    else:
                                        fila_met[jugador] = int(valor)
                                else:
                                    fila_met[jugador] = '-'
                            datos_tabla_pas.append(fila_met)

                    if datos_tabla_pas:
                        df_tabla_pas = pd.DataFrame(datos_tabla_pas)
                        st.dataframe(
                            df_tabla_pas,
                            use_container_width=True,
                            hide_index=True,
                            height=250
                        )

                        st.markdown("**Comparación de Pases**")

                        metricas_graf_pas = ['Assists', 'Key passes', 'Big chances created']
                        metricas_disp_pas = [m for m in metricas_graf_pas if m in df_comparacion.columns]

                        if metricas_disp_pas:
                            df_plot_pas = df_comparacion[['Name'] + metricas_disp_pas].copy()
                            fig_pas = px.bar(
                                df_plot_pas.melt(id_vars='Name', value_vars=metricas_disp_pas,
                                                 var_name='Métrica', value_name='Valor'),
                                x='Name',
                                y='Valor',
                                color='Métrica',
                                barmode='group',
                                title="Stats de Creación",
                                labels={'Name': 'Jugador', 'Valor': 'Cantidad', 'Métrica': 'Métrica'},
                            )
                            st.plotly_chart(fig_pas, use_container_width=True)

                # ============================================
                # RESUMEN FINAL - QUIÉN ES MEJOR EN QUÉ
                # ============================================

                st.markdown("---")
                st.markdown("### 🏆 Resumen: Quién destaca en cada área")

                col_res1, col_res2, col_res3 = st.columns(3)

                with col_res1:
                    st.markdown("**⚽ Ofensiva**")
                    if 'Goals' in df_comparacion.columns:
                        mejor_goleador = df_comparacion.nlargest(1, 'Goals')['Name'].values[0]
                        st.success(f"🥇 **Goles:** {mejor_goleador}")

                    if 'Succ. dribbles' in df_comparacion.columns:
                        mejor_regateador = df_comparacion.nlargest(1, 'Succ. dribbles')['Name'].values[0]
                        st.success(f"🏃 **Regates:** {mejor_regateador}")

                with col_res2:
                    st.markdown("**🛡️ Defensiva**")
                    if 'Tackles' in df_comparacion.columns:
                        mejor_tackleador = df_comparacion.nlargest(1, 'Tackles')['Name'].values[0]
                        st.success(f"⚔️ **Tackles:** {mejor_tackleador}")

                    if 'Interceptions' in df_comparacion.columns:
                        mejor_interceptor = df_comparacion.nlargest(1, 'Interceptions')['Name'].values[0]
                        st.success(f"🛡️ **Intercepciones:** {mejor_interceptor}")

                with col_res3:
                    st.markdown("**📡 Pases**")
                    if 'Assists' in df_comparacion.columns:
                        mejor_asistidor = df_comparacion.nlargest(1, 'Assists')['Name'].values[0]
                        st.success(f"🎯 **Asistencias:** {mejor_asistidor}")

                    if 'Accurate passes %' in df_comparacion.columns:
                        mejor_precision = df_comparacion.nlargest(1, 'Accurate passes %')['Name'].values[0]
                        st.success(f"📈 **Precisión:** {mejor_precision}")

                # ============================================
                # EXPORTAR COMPARACIÓN
                # ============================================

                st.markdown("---")

                reporte_completo = []
                for jugador in jugadores_seleccionados:
                    fila_j = df_comparacion[df_comparacion['Name'] == jugador].head(1)
                    if fila_j.empty:
                        continue
                    data = fila_j.iloc[0]
                    reporte_completo.append({
                        'Jugador': jugador,
                        'Equipo': data.get('Team', 'N/A'),
                        'Posición': data.get('Position', 'N/A'),
                        'Goles': int(data.get('Goals', 0)) if pd.notna(data.get('Goals', None)) else 0,
                        'Asistencias': int(data.get('Assists', 0)) if pd.notna(data.get('Assists', None)) else 0,
                        'Tackles': int(data.get('Tackles', 0)) if pd.notna(data.get('Tackles', None)) else 0,
                        'Precisión Pases %': f"{data.get('Accurate passes %', 0):.1f}%"
                    })

                if reporte_completo:
                    df_reporte = pd.DataFrame(reporte_completo)
                    csv_comparacion = df_reporte.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Descargar Comparación (CSV)",
                        data=csv_comparacion,
                        file_name=f'comparacion_jugadores_{pd.Timestamp.now().strftime("%Y%m%d")}.csv',
                        mime='text/csv'
                    )


# --- TAB 5: DATOS COMPLETOS ---
with tab5:
    st.subheader("📋 Base de Datos Completa (sin ranking)")

    if df_filtrado.empty:
        st.info("No hay jugadores bajo los filtros actuales. Limpia filtros para ver toda la base de datos.")
    else:
        # Ordenar alfabéticamente por nombre y eliminar columnas tipo '#' o similares
        df_completo = df_filtrado.copy()
        if 'Name' in df_completo.columns:
            df_completo = df_completo.sort_values('Name', ascending=True)

        columnas_completas = [c for c in df_completo.columns if not c.startswith('#')]
        df_completo = df_completo[columnas_completas]

        st.dataframe(
            df_completo,
            use_container_width=True,
            height=700
        )

        # Botón de descarga con la base mostrada
        csv = df_completo.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV (vista actual)",
            data=csv,
            file_name='la_liga_scouting_completo.csv',
            mime='text/csv'
        )


# ============================================
# FOOTER
# ============================================

st.markdown("---")

st.markdown("**Datos:** Sofascore | **Dashboard by:** José Granado")
