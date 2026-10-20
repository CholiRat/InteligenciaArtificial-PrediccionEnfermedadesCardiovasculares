"""Genera y cachea en disco los datos ya preprocesados (imputados,
normalizados y con SMOTENC aplicado) de los 5 pliegues, para que los 4
notebooks de modelo (LR, RF, XGBoost, SVM) no tengan que recalcular lo
mismo cada uno por su cuenta.

Correr una sola vez, desde la raiz del proyecto o desde scripts/:
    python scripts/preprocesar_pliegues.py

Genera en ../data_procesada/:
    fold_{i}_train.parquet              (i = 0..4, con SMOTENC)
    fold_{i}_train_sin_smotenc.parquet  (i = 0..4, solo imputado y normalizado,
                                          para la comparacion con class weighting)
    fold_{i}_test.parquet               (i = 0..4, sin SMOTENC)
    tuning_train_interno.parquet        (80% del train del pliegue 0, con SMOTENC)
    tuning_validacion_interna.parquet   (20% del train del pliegue 0, sin SMOTENC)

Es deterministico: mismo pl.RANDOM_STATE siempre, asi que regenerar estos
archivos produce exactamente los mismos resultados. Por eso no se suben al
repositorio (ver .gitignore).
"""

import os
import time

import pandas as pd
from sklearn.model_selection import train_test_split

import pipeline as pl

AQUI = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(AQUI, "..", "Dataset", "brfss_2024_cvd_fairness_clean.csv")
OUT_DIR = os.path.join(AQUI, "..", "data_procesada")


def guardar(X, y, nombre):
    tabla = X.copy()
    tabla[pl.TARGET_COL] = y.to_numpy()
    tabla.to_parquet(os.path.join(OUT_DIR, nombre), index=False)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(DATASET_PATH)
    df = pl.construir_target(df)
    X, y, _ = pl.separar_X_y_protegidas(df)
    folds = pl.generar_folds(X, y, n_splits=5)

    for i, (tr_idx, te_idx) in enumerate(folds):
        inicio = time.time()
        X_train, X_test = X.iloc[tr_idx].reset_index(drop=True), X.iloc[te_idx].reset_index(drop=True)
        y_train, y_test = y.iloc[tr_idx].reset_index(drop=True), y.iloc[te_idx].reset_index(drop=True)

        X_train, X_test = pl.imputar_proporcional(X_train, X_test)
        X_train, X_test = pl.normalizar(X_train, X_test)
        X_train_s, y_train_s = pl.aplicar_smote(X_train, y_train)

        guardar(X_train_s, y_train_s, f"fold_{i}_train.parquet")
        guardar(X_train, y_train, f"fold_{i}_train_sin_smotenc.parquet")
        guardar(X_test, y_test, f"fold_{i}_test.parquet")
        print(f"pliegue {i} listo ({time.time() - inicio:.0f}s)")

    inicio = time.time()
    tr_idx0, _ = folds[0]
    X_train0 = X.iloc[tr_idx0].reset_index(drop=True)
    y_train0 = y.iloc[tr_idx0].reset_index(drop=True)

    X_tr_int, X_val_int, y_tr_int, y_val_int = train_test_split(
        X_train0, y_train0, test_size=0.2, stratify=y_train0, random_state=pl.RANDOM_STATE,
    )
    X_tr_int, X_val_int = pl.imputar_proporcional(X_tr_int, X_val_int)
    X_tr_int, X_val_int = pl.normalizar(X_tr_int, X_val_int)
    X_tr_int_s, y_tr_int_s = pl.aplicar_smote(X_tr_int, y_tr_int)

    guardar(X_tr_int_s, y_tr_int_s, "tuning_train_interno.parquet")
    guardar(X_val_int, y_val_int, "tuning_validacion_interna.parquet")
    print(f"particion de ajuste de hiperparametros lista ({time.time() - inicio:.0f}s)")


if __name__ == "__main__":
    main()
