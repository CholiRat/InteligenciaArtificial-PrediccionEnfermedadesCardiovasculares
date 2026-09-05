import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"

## Calcular los porcentajes reales a partir del dataset limpio 
df = pd.read_csv("../Dataset/brfss_2024_cvd_fairness_clean.csv")
cvd_cols = ["CVDINFR4", "CVDCRHD4", "CVDSTRK3"]
df_valid = df.dropna(subset=cvd_cols).copy()
df_valid["riesgo"] = (
    (df_valid["CVDINFR4"] == 1) | (df_valid["CVDCRHD4"] == 1) | (df_valid["CVDSTRK3"] == 1)
).astype(int)

overall = df_valid["riesgo"].mean() * 100

genero = (df_valid.groupby("_SEX")["riesgo"].mean() * 100)
raza = (df_valid.groupby("_RACE")["riesgo"].mean() * 100)

# Etiquetas segun el codebook estandar de BRFSS para _RACE
raza_labels = {
    1.0: "Blanca", 2.0: "Negra", 3.0: "Indígena / nativa de Alaska",
    4.0: "Asiática", 5.0: "Nativa de Hawai / Pacífico", 6.0: "Otra raza",
    7.0: "Multirracial", 8.0: "Hispánica",
}

labels_values = [("Hombres", genero.get(1.0)), ("Mujeres", genero.get(2.0))]
raza_items = sorted(
    [(raza_labels[k], v) for k, v in raza.items() if k in raza_labels],
    key=lambda x: -x[1],
)
ordered = labels_values + raza_items
labels = [x[0] for x in ordered]
values = [x[1] for x in ordered]
is_genero = [True, True] + [False] * len(raza_items)

fig, ax = plt.subplots(figsize=(3.4, 2.75))
y_pos = range(len(labels))
colors = ["#4d4d4d" if g else "#a6a6a6" for g in is_genero]

bars = ax.barh(list(y_pos), values, color=colors, edgecolor="black", linewidth=0.6, height=0.72)
ax.set_yticks(list(y_pos))
ax.set_yticklabels(labels, fontsize=8)
ax.axhline(1.5, color="lightgray", linewidth=0.8)

ax.axvline(overall, color="black", linestyle="--", linewidth=1.1)
ax.set_ylim(len(labels) - 0.3, -1.4)
ax.text(overall + 0.3, -1.15, f"Promedio general: {overall:.2f}%",
        fontsize=7.3, va="center", ha="left")

for bar, val in zip(bars, values):
    ax.text(val + 0.25, bar.get_y() + bar.get_height() / 2, f"{val:.2f}%",
            va="center", fontsize=7.3)

ax.set_xlabel("% con riesgo cardiovascular", fontsize=8.5)
ax.set_xlim(0, 19.5)
ax.tick_params(axis="x", labelsize=7.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("../Documentacion/balance_riesgo_grupos.png", dpi=300, bbox_inches="tight")
print("ok")
