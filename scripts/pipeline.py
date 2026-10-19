"""Pipeline de preprocesamiento compartido para los 4 modelos (LR, RF, XGBoost, SVM).

Cada funcion que recibe train/test por separado se ajusta solo con el train
de ese pliegue, para evitar fuga de datos entre pliegues.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE

RANDOM_STATE = 42

TARGET_SOURCE_COLS = ["CVDINFR4", "CVDCRHD4", "CVDSTRK3"]
TARGET_COL = "riesgo_cardiovascular"
PROTECTED_COLS = ["_SEX", "_RACE", "_INCOMG1"]
SUFIJOS_PROTEGIDAS = {"_SEX": "sexo", "_RACE": "raza", "_INCOMG1": "ingreso"}
CONTINUOUS_COLS = ["_AGE80", "WEIGHT2", "HEIGHT3", "_BMI5", "_DRNKWK3", "PHYSHLTH", "MENTHLTH"]


def construir_target(df):
    """Crea riesgo_cardiovascular (1 si CVDINFR4/CVDCRHD4/CVDSTRK3 = Si) y
    descarta las filas donde alguna de las tres quedo sin responder."""
    df = df.dropna(subset=TARGET_SOURCE_COLS).copy()
    es_positivo = (df[TARGET_SOURCE_COLS] == 1).any(axis=1)
    df[TARGET_COL] = es_positivo.astype(int)
    return df


def separar_X_y_protegidas(df):
    """Separa predictoras (X, incluye las protegidas), objetivo (y) y una
    copia aparte de sexo/raza/ingreso para la evaluacion de equidad."""
    y = df[TARGET_COL]
    protegidas = df[PROTECTED_COLS].copy()
    X = df.drop(columns=TARGET_SOURCE_COLS + [TARGET_COL])
    return X, y, protegidas


def generar_folds(X, y, n_splits=5):
    """Indices de Stratified K-Fold (mismo random_state para los 4 modelos)."""
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    return list(skf.split(X, y))


def imputar_proporcional(X_train, X_test, random_state=RANDOM_STATE):
    """Rellena nulos muestreando de la distribucion empirica del train de
    ese pliegue (sirve igual para columnas categoricas y continuas)."""
    rng = np.random.default_rng(random_state)
    X_train = X_train.copy()
    X_test = X_test.copy()
    for col in X_train.columns:
        observados = X_train[col].dropna().to_numpy()
        if observados.size == 0:
            continue
        mascara_train = X_train[col].isna()
        if mascara_train.any():
            X_train.loc[mascara_train, col] = rng.choice(observados, size=mascara_train.sum())
        mascara_test = X_test[col].isna()
        if mascara_test.any():
            X_test.loc[mascara_test, col] = rng.choice(observados, size=mascara_test.sum())
    return X_train, X_test


def normalizar(X_train, X_test, columnas=CONTINUOUS_COLS):
    """MinMax Scaling (0-1) ajustado solo con el train, aplicado a las
    columnas continuas, se aplica a los 4 modelos por igual (mismo pipeline)."""
    X_train = X_train.copy()
    X_test = X_test.copy()
    scaler = MinMaxScaler()
    X_train[columnas] = scaler.fit_transform(X_train[columnas])
    X_test[columnas] = scaler.transform(X_test[columnas])
    return X_train, X_test


def aplicar_smote(X_train, y_train, random_state=RANDOM_STATE):
    """Sobremuestreo sintetico de la clase minoritaria, solo sobre el train.
    Alternativa exploratoria: usar class_weight/scale_pos_weight en el
    modelo en vez de llamar esta funcion (ver notebook de cada modelo)."""
    smote = SMOTE(random_state=random_state)
    return smote.fit_resample(X_train, y_train)


def ingreso_observado(df):
    """Bandera de si _INCOMG1 era un valor real, capturada ANTES de imputar."""
    return df["_INCOMG1"].notna()


def _tpr(y_true, y_pred):
    positivos = y_true == 1
    if positivos.sum() == 0:
        return np.nan
    return (y_pred[positivos] == 1).mean()


def _fpr(y_true, y_pred):
    negativos = y_true == 0
    if negativos.sum() == 0:
        return np.nan
    return (y_pred[negativos] == 1).mean()


def _calibracion(y_true, y_proba):
    suma_y = y_true.sum()
    if suma_y == 0:
        return np.nan
    return y_proba.sum() / suma_y


def _metricas_por_grupo(y_true, y_pred, y_proba, grupos):
    filas = []
    for valor_grupo in pd.Series(grupos).dropna().unique():
        mascara = (grupos == valor_grupo).to_numpy()
        filas.append({
            "grupo": valor_grupo,
            "n": int(mascara.sum()),
            "tpr": _tpr(y_true[mascara], y_pred[mascara]),
            "fpr": _fpr(y_true[mascara], y_pred[mascara]),
            "calibracion": _calibracion(y_true[mascara], y_proba[mascara]),
        })
    return pd.DataFrame(filas)


def evaluar(y_test, y_pred, y_proba, protegidas_test):
    """Calcula AUROC global y EOD/disparidad de FPR/desviacion de calibracion
    por cada atributo protegido (sexo, raza, ingreso).

    Devuelve (resumen, detalle): resumen es un dict plano listo para
    agregarse como una fila de results/metrics_<modelo>.csv; detalle es
    un dict {columna_protegida: DataFrame con una fila por grupo, incluyendo
    el tamaño de muestra n de cada grupo}.
    """
    y_test = np.asarray(y_test)
    y_pred = np.asarray(y_pred)
    y_proba = np.asarray(y_proba)

    resumen = {"auroc": roc_auc_score(y_test, y_proba)}
    detalle = {}

    for col in PROTECTED_COLS:
        tabla = _metricas_por_grupo(y_test, y_pred, y_proba, protegidas_test[col])
        detalle[col] = tabla
        sufijo = SUFIJOS_PROTEGIDAS[col]
        resumen[f"eod_{sufijo}"] = tabla["tpr"].max() - tabla["tpr"].min()
        resumen[f"fpr_disp_{sufijo}"] = tabla["fpr"].max() - tabla["fpr"].min()
        resumen[f"calib_desv_{sufijo}"] = (tabla["calibracion"] - 1).abs().max()

    return resumen, detalle
