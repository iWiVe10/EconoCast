import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from econocast.params import *

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza y transformación inicial del dataset"""
    print("\n⌛ Limpiando datos")
    df = df.map(lambda x: str(x).replace(",", "") if isinstance(x, str) else x)
    df = df.apply(pd.to_numeric, errors="coerce")
    df.dropna(how="all", axis=1, inplace=True)  # Elimina columnas completamente vacías
    df.dropna(how="all", axis=0, inplace=True)  # Elimina filas completamente vacías
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    df = df[df['anio'] >= 2005]


    print("\n✅ Datos limpios")
    return df


def preprocess_data(df):
    print("\n⌛ Escalando datos")
    scaler = MinMaxScaler()

    df_scaled = df.copy()
    if TARGET in df.columns:
        df_scaled[TARGET] = scaler.fit_transform(df[[TARGET]])
    else:
        raise ValueError("❌ Error: La columna 'indice_ipc_general' no existe en los datos.")

    print(f"📏 Min IPC: {scaler.data_min_[0]}, Max IPC: {scaler.data_max_[0]}")
    print("\n✅ Datos escalados correctamente")
    return df_scaled, scaler
