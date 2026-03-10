import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración básica (estilo que no da error)
plt.style.use('ggplot')

print("="*70)
print("GENERANDO REPORTES DE VALOR - LA LIGA")
print("="*70)

# ============================================
# 1. CARGAR DATOS (Ahora desde el CSV final)
# ============================================
archivo = 'la_liga_stats_FINAL.csv'

try:
    df = pd.read_csv(archivo)
    # Limpieza de nombres de columnas por si hay espacios
    df.columns = df.columns.str.strip()
    print(f"✅ Archivo {archivo} cargado correctamente.")
    print(f"📊 Total de jugadores: {len(df)}")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo {archivo}")
    exit()

# ============================================
# 2. GRÁFICO: EFECTIVIDAD REAL (Goals vs xG)
# ============================================
# Este gráfico es el que le importa a un scout: ¿Quién mete más de lo que debería?
print("\n2. Generando Gráfico de Eficiencia (Goals vs xG)...")

# Limpiamos posibles NaNs en las columnas clave
df_plot = df.dropna(subset=['Goals', 'Expected goals (xG)']).copy()

plt.figure(figsize=(12, 8))

# Scatter plot
plt.scatter(df_plot['Expected goals (xG)'], df_plot['Goals'], 
            s=100, alpha=0.6, c='#3498db', edgecolors='white')

# Línea de "Normalidad" (Si metés lo mismo que tu xG)
max_val = max(df_plot['Goals'].max(), df_plot['Expected goals (xG)'].max())
plt.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Eficiencia Media')

# Etiquetar solo a los 10 mejores goleadores para no ensuciar el gráfico
top_10 = df_plot.nlargest(10, 'Goals')
for _, row in top_10.iterrows():
    plt.annotate(row['Name'], (row['Expected goals (xG)'], row['Goals']), 
                 xytext=(5,5), textcoords='offset points', fontsize=9)

plt.xlabel('Goles Esperados (xG)', fontweight='bold')
plt.ylabel('Goles Reales', fontweight='bold')
plt.title('Detección de Killers: Goles Reales vs. xG', fontsize=15, pad=20)
plt.legend()
plt.tight_layout()
plt.savefig('futbol_eficiencia.png', dpi=300)
print("   ✅ Guardado: futbol_eficiencia.png")

# ============================================
# 3. GRÁFICO: VOLUMEN DE PASES
# ============================================
print("3. Generando Top 10 Pasadores...")

# Ajustamos al nombre de columna probable de SofaScore
col_pases = 'Accurate passes' if 'Accurate passes' in df.columns else 'Passes'
top_pasadores = df.nlargest(10, col_pases)

plt.figure(figsize=(10, 6))
plt.barh(top_pasadores['Name'], top_pasadores[col_pases], color='#2ecc71')
plt.gca().invert_yaxis() # Para que el #1 esté arriba
plt.title('Top 10 Pasadores (Volumen de Juego)')
plt.xlabel('Pases Precisos')
plt.tight_layout()
plt.savefig('futbol_pasadores.png', dpi=300)
print("   ✅ Guardado: futbol_pasadores.png")

print("\n" + "="*70)
print("✅ REPORTES GENERADOS")
print("="*70)