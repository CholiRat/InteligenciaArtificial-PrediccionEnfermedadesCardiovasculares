import pandas as pd

df = pd.read_csv("../Dataset/brfss_2024_cvd_fairness_clean.csv")

## 1. Se crea la variable objetivo: riesgo cardiovascular
## Positivo (1) si tuvo infarto, enfermedad coronaria, o ACV. Negativo (0) si no tuvo ninguna.
## Se descartan filas donde falte información en las 3 columnas relevantes.
cvd_cols = ["CVDINFR4", "CVDCRHD4", "CVDSTRK3"]
df_valid = df.dropna(subset=cvd_cols).copy()

df_valid["riesgo_cardiovascular"] = (
    (df_valid["CVDINFR4"] == 1) |
    (df_valid["CVDCRHD4"] == 1) |
    (df_valid["CVDSTRK3"] == 1)
).astype(int)

print(f"Filas válidas (con las 3 variables de CVD completas): {len(df_valid)}")
print()

## 2. Se realiza el balance general
print("=== Balance general de la variable objetivo ===")
conteo = df_valid["riesgo_cardiovascular"].value_counts()
porcentaje = df_valid["riesgo_cardiovascular"].value_counts(normalize=True) * 100
resumen = pd.DataFrame({"conteo": conteo, "%": porcentaje.round(2)})
resumen.index = resumen.index.map({0: "Sin riesgo (0)", 1: "Con riesgo (1)"})
print(resumen)
print()

## 3. Se realiza el balance por género
print("=== Balance por género (_SEX: 1=Hombre, 2=Mujer) ===")
tabla_genero = pd.crosstab(df_valid["_SEX"], df_valid["riesgo_cardiovascular"], normalize="index") * 100
tabla_genero.columns = ["% Sin riesgo", "% Con riesgo"]
tabla_genero.index = tabla_genero.index.map({1.0: "Hombre", 2.0: "Mujer"})
print(tabla_genero.round(2))
print()

# 4. Balance por raza (otro subgrupo demográfico relevante para fairness)
print("=== Balance por raza (_RACE) ===")
tabla_raza = pd.crosstab(df_valid["_RACE"], df_valid["riesgo_cardiovascular"], normalize="index") * 100
tabla_raza.columns = ["% Sin riesgo", "% Con riesgo"]
print(tabla_raza.round(2))