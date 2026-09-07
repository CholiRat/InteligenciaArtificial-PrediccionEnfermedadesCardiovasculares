# Diccionario de Datos

Dataset: `brfss_2024_cvd_fairness_clean.csv` (457,670 filas, 33 columnas), derivado del *Behavioral Risk Factor Surveillance System* (BRFSS) 2024 del CDC.

Los códigos de "no sabe / rechazó responder" del BRFSS crudo (usualmente 7, 9, 77, 99 según la variable) ya fueron convertidos a valor faltante antes de generar este archivo (ver `scripts/extract.py`), así que los valores listados abajo son los únicos que deberían aparecer en los datos limpios.

**Nota sobre precisión**: la codificación de las variables con muchas categorías (`PRIMINS2`, `EMPLOY1`, `MARITAL`) se documenta aquí a nivel de resumen. Antes de la entrega final, verificar contra el codebook oficial de BRFSS 2024 ([cdc.gov/brfss](https://www.cdc.gov/brfss)) si se necesita el detalle exacto de cada categoría.

Los porcentajes de valores faltantes fueron calculados directamente sobre el dataset limpio (no son estimados).

## 1. Demografía y variables socioeconómicas (14)

| Variable | Descripción | Codificación | % Faltante |
|---|---|---|---|
| `_STATE` | Estado o territorio de residencia (código FIPS) | 01-56 = estados; 11 = Distrito de Columbia; 66 = Guam; 72 = Puerto Rico; 78 = Islas Vírgenes de EE. UU. | 0.00% |
| `_SEX` | Sexo (variable calculada) | 1 = Hombre; 2 = Mujer | 0.00% |
| `_AGEG5YR` | Grupo de edad en categorías de 5 años | 1 = 18-24 ... 13 = 80+ (13 categorías) | 0.00% |
| `_AGE80` | Edad imputada en años (topada en 80) | 18-80 | 0.00% |
| `_RACE` | Raza / etnia (variable calculada) | 1 = Blanca no hispana; 2 = Negra no hispana; 3 = Indígena americana / nativa de Alaska no hispana; 4 = Asiática no hispana; 5 = Nativa de Hawái / Islas del Pacífico no hispana; 6 = Otra raza no hispana; 7 = Multirracial no hispana; 8 = Hispana | 1.99% |
| `_HISPANC` | Origen hispano o latino (variable calculada) | 1 = Hispano; 2 = No hispano | 1.15% |
| `EDUCA` | Nivel educativo más alto alcanzado | 1 = Nunca asistió / solo kínder; 2 = Primaria (1°-8°); 3 = Secundaria incompleta; 4 = Secundaria completa (o GED); 5 = Universidad/técnico incompleto; 6 = Universitario graduado | 0.52% |
| `_INCOMG1` | Categoría de ingreso familiar anual (variable calculada) | 1 = <\$15,000; 2 = \$15,000-\$24,999; 3 = \$25,000-\$34,999; 4 = \$35,000-\$49,999; 5 = \$50,000-\$99,999; 6 = \$100,000-\$199,999; 7 = ≥\$200,000 | 19.10% |
| `MARITAL` | Estado civil | 1 = Casado/a; 2 = Divorciado/a; 3 = Viudo/a; 4 = Separado/a; 5 = Nunca casado/a; 6 = Pareja de hecho | 0.92% |
| `VETERAN3` | ¿Ha servido en las fuerzas armadas de EE. UU.? | 1 = Sí; 2 = No | 0.56% |
| `EMPLOY1` | Situación laboral actual | 1 = Empleado (cuenta ajena); 2 = Trabajador independiente; 3 = Desempleado ≥1 año; 4 = Desempleado <1 año; 5 = Ama/o de casa; 6 = Estudiante; 7 = Jubilado/a; 8 = Incapacitado para trabajar | 1.84% |
| `RENTHOM1` | Tenencia de la vivienda | 1 = Propia; 2 = Alquilada; 3 = Otro arreglo | 0.86% |
| `PRIMINS2` | Tipo de seguro médico principal | Categorías 1-9 según fuente (empleador, comprado directamente, Medicare, Medicaid, militar/VA, Indian Health Service, etc.); ver codebook oficial para el detalle exacto | 4.05% |
| `MEDCOST1` | ¿En los últimos 12 meses no pudo ver a un médico por el costo? | 1 = Sí; 2 = No | 0.37% |

## 2. Antropometría (3)

| Variable | Descripción | Codificación | % Faltante |
|---|---|---|---|
| `WEIGHT2` | Peso reportado, ya convertido a kilogramos | Valor continuo (kg) | 7.95% |
| `HEIGHT3` | Estatura reportada, ya convertida a centímetros | Valor continuo (cm) | 5.25% |
| `_BMI5` | Índice de Masa Corporal (variable calculada) | Valor continuo (kg/m²) | 9.40% |

## 3. Antecedentes cardiovasculares y comorbilidades (9)

| Variable | Descripción | Codificación | % Faltante |
|---|---|---|---|
| `CVDINFR4` | ¿Alguna vez le dijeron que tuvo un infarto? | 1 = Sí; 2 = No | 0.68% |
| `CVDCRHD4` | ¿Alguna vez le dijeron que tuvo enfermedad coronaria o angina? | 1 = Sí; 2 = No | 1.00% |
| `CVDSTRK3` | ¿Alguna vez le dijeron que tuvo un accidente cerebrovascular (ACV)? | 1 = Sí; 2 = No | 0.32% |
| `DIABETE4` | ¿Le han diagnosticado diabetes? | 1 = Sí; 2 = Sí, solo durante el embarazo; 3 = No; 4 = Prediabetes / diabetes límite | 0.23% |
| `CHCKDNY2` | ¿Le han diagnosticado enfermedad renal crónica? | 1 = Sí; 2 = No | 0.43% |
| `HAVARTH4` | ¿Le han diagnosticado artritis? | 1 = Sí; 2 = No | 0.56% |
| `ADDEPEV3` | ¿Le han diagnosticado depresión? | 1 = Sí; 2 = No | 0.58% |
| `CHCCOPD3` | ¿Le han diagnosticado EPOC, enfisema o bronquitis crónica? | 1 = Sí; 2 = No | 0.48% |
| `ASTHMA3` | ¿Le han diagnosticado asma? | 1 = Sí; 2 = No | 0.41% |

`CVDINFR4`, `CVDCRHD4` y `CVDSTRK3` son las tres columnas que definen la variable objetivo `riesgo_cardiovascular` (ver Sección IV-A del paper); se excluyen del conjunto de predictores para evitar fuga de datos (Sección V-G).

## 4. Estilo de vida (4)

| Variable | Descripción | Codificación | % Faltante |
|---|---|---|---|
| `_SMOKER3` | Estatus de fumador (variable calculada) | 1 = Fumador actual (diario); 2 = Fumador actual (algunos días); 3 = Exfumador; 4 = Nunca fumó | 7.00% |
| `_RFDRHV9` | Consumo elevado de alcohol (variable calculada) | 1 = No; 2 = Sí (consumo elevado según umbral por sexo) | 10.20% |
| `_DRNKWK3` | Consumo promedio de bebidas alcohólicas por semana (variable calculada) | Valor continuo | 10.20% |
| `_TOTINDA` | ¿Realizó actividad física fuera del trabajo en los últimos 30 días? | 1 = Sí; 2 = No | 0.29% |

## 5. Salud percibida (3)

| Variable | Descripción | Codificación | % Faltante |
|---|---|---|---|
| `GENHLTH` | Percepción general de salud | 1 = Excelente; 2 = Muy buena; 3 = Buena; 4 = Regular; 5 = Mala | 0.29% |
| `PHYSHLTH` | Días (de los últimos 30) en que la salud física no fue buena | 0-30 | 2.42% |
| `MENTHLTH` | Días (de los últimos 30) en que la salud mental no fue buena | 0-30 | 1.78% |

## Variables protegidas (análisis de equidad)

`_SEX`, `_RACE` e `_INCOMG1` se usan como atributos protegidos para medir disparidad de desempeño entre grupos (ver Sección IV-A y IV-F del paper).
