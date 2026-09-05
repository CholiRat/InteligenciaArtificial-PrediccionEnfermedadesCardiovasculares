# Predicción de Enfermedades Cardiovasculares

Este proyecto se enfoca en la predicción de enfermedades cardiovasculares utilizando técnicas de inteligencia artificial. Para el desarrollo del análisis, se seleccionó el conjunto de datos BRFSS 2024, el cual proviene de encuestas telefónicas sobre factores de riesgo de salud. El proceso de preparación de los datos involucró el procesamiento del archivo original en formato `.xpt`, del cual se seleccionaron 33 atributos de interés.

Adicionalmente, el repositorio incluye un documento formal elaborado en LaTeX que contiene la documentación del proyecto y sus respectivas bibliografías.

## Estructura del repositorio

- `Dataset/`: dataset limpio (`brfss_2024_cvd_fairness_clean.csv`).
- `scripts/`: scripts de extracción, análisis exploratorio y generación de figuras.
- `Documentacion/`: artículo en LaTeX (`main.tex`), referencias y figuras.

## Cómo correr los scripts

```bash
pip install -r requirements.txt
cd scripts
python balance_check.py              # desbalance de clases por género y raza
python gen_balance_chart.py          # regenera la Figura 2 del paper
```

## Integrantes

- Daniel de Jesús Alemán Ruiz | 2023051957 
- Sebastián Rodríguez Sánchez | 2023074446 
- Lindsay Marín Sánchez 

## Información del Curso

- **Curso:** IC6200 — Inteligencia Artificial
- **Profesor:** Kenneth Obando Rodríguez
- **II Semestre, 2026**