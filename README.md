# Predicción de Enfermedades Cardiovasculares

## Integrantes

- Daniel de Jesús Alemán Ruiz | 2023051957
- Sebastián Rodríguez Sánchez | 2023074446
- Lindsay Marín Sánchez       | 2024163904

## Información del Curso

- **Curso:** IC6200 — Inteligencia Artificial
- **Profesor:** Kenneth Obando Rodríguez
- **II Semestre, 2026**

---



Este proyecto se enfoca en la predicción de enfermedades cardiovasculares utilizando técnicas de inteligencia artificial. Para el desarrollo del análisis, se seleccionó el conjunto de datos BRFSS 2024, el cual proviene de encuestas telefónicas sobre factores de riesgo de salud. El proceso de preparación de los datos involucró el procesamiento del archivo original en formato `.xpt`, del cual se seleccionaron 33 atributos de interés.

Adicionalmente, el repositorio incluye un documento formal elaborado en LaTeX que contiene la documentación del proyecto y sus respectivas bibliografías.

## Estructura del repositorio

- `Dataset/`: dataset limpio (`brfss_2024_cvd_fairness_clean.csv`) y diccionario de datos.
- `scripts/`: scripts de extracción, análisis exploratorio, generación de figuras, y el pipeline de preprocesamiento compartido (`pipeline.py`, `preprocesar_pliegues.py`).
- `notebooks/`: un cuaderno de Jupyter por modelo (`03_xgboost.ipynb`, etc.), donde se entrena y evalúa cada uno bajo el mismo protocolo experimental.
- `results/`: métricas de cada modelo por pliegue, en `.csv` (`metrics_<modelo>.csv`, `detalle_<modelo>.csv`).
- `data_procesada/`: caché local de los datos ya preprocesados por pliegue (generada por `preprocesar_pliegues.py`). **No se sube al repositorio** (ver `.gitignore`); cada integrante la genera una vez en su propia máquina.
- `Documentacion/`: artículo en LaTeX (`main.tex`), referencias y figuras.

## Cómo correr los scripts de análisis exploratorio

```bash
pip install -r requirements.txt
cd scripts
python balance_check.py              # desbalance de clases por género y raza
python gen_balance_chart.py          # regenera la Figura 2 del paper
python gen_missing_values_chart.py   # regenera la Figura 4 del paper
```

## Cómo correr los notebooks de modelado

Antes de abrir cualquier notebook de `notebooks/`, hay que generar el caché de datos preprocesados **una sola vez por máquina** (tarda unos 15 minutos, porque incluye SMOTENC, que es lento):

```bash
pip install -r requirements.txt
python scripts/preprocesar_pliegues.py
```

Esto genera `data_procesada/` con los 5 pliegues ya imputados, normalizados y balanceados (y la partición de ajuste de hiperparámetros). Una vez generado, cada notebook de `notebooks/` solo lee esos archivos — no hace falta volver a correr el script salvo que cambie `scripts/pipeline.py` (en ese caso, hay que regenerar el caché para que quede consistente).

