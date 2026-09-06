import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"

# --- Calcular los porcentajes reales de valores faltantes ---
df = pd.read_csv("../Dataset/brfss_2024_cvd_fairness_clean.csv")

# Variables mostradas en la Figura 4 del paper: las de mayor % de faltantes
# entre los predictores, mas CVDCRHD4 (una de las 3 columnas que definen la
# variable objetivo), incluida como referencia y no por ranking.
columnas = ["_INCOMG1", "_DRNKWK3", "_RFDRHV9", "_BMI5", "WEIGHT2",
            "_SMOKER3", "HEIGHT3", "CVDCRHD4"]

pct_faltante = (df[columnas].isna().mean() * 100).sort_values(ascending=False)

labels = list(pct_faltante.index)
values = list(pct_faltante.values)

fig, ax = plt.subplots(figsize=(3.4, 3.0))
y_pos = range(len(labels))
colors = ["#4d4d4d"] + ["#a6a6a6"] * (len(labels) - 1)

bars = ax.barh(list(y_pos), values, color=colors, edgecolor="black", linewidth=0.6, height=0.65)
ax.set_yticks(list(y_pos))
ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis()

for bar, val in zip(bars, values):
    ax.text(val + 0.4, bar.get_y() + bar.get_height() / 2, f"{val:.2f}%",
            va="center", fontsize=7.5)

ax.set_xlabel("% de valores faltantes", fontsize=8.5)
ax.set_xlim(0, max(values) + 3.5)
ax.tick_params(axis="x", labelsize=7.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("../Documentacion/valores_faltantes.png", dpi=300, bbox_inches="tight")
print("ok")
print(pct_faltante.round(2))
