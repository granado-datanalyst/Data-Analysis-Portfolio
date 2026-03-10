import pandas as pd

archivo = r'C:\Users\JOSE GRANADO PC\desktop\futbol-data\sofascore top 200 main stats.xlsx'

# Cargamos las hojas
df_at = pd.read_excel(archivo, sheet_name=0)
df_de = pd.read_excel(archivo, sheet_name=1)
df_pa = pd.read_excel(archivo, sheet_name=2)

# Extraemos los nombres tal cual están (sin limpiar nada para ver el error real)
at = set(df_at['Name'].dropna().astype(str))
de = set(df_de['Name'].dropna().astype(str))
pa = set(df_pa['Name'].dropna().astype(str))

print(f"--- RECUENTO REAL ---")
print(f"Nombres en Ataque: {len(at)}")
print(f"Nombres en Defensa: {len(de)}")
print(f"Nombres en Pases: {len(pa)}")

print("\n" + "="*60)
print("🔍 JUGADORES QUE ESTÁN EN ATAQUE PERO NO EN DEFENSA:")
print(at - de if at - de else "Ninguno")

print("\n🔍 JUGADORES QUE ESTÁN EN DEFENSA PERO NO EN ATAQUE:")
print(de - at if de - at else "Ninguno")
print("="*60)