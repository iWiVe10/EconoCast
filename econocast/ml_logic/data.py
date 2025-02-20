import pandas as pd
import joblib
from econocast.params import *

def load_data() -> pd.DataFrame:
    """
    Obtener la data cruda
    """
    file_path = os.path.join(LOCAL_DATA_PATH, FILE_DATA)
    df = pd.read_csv(file_path)

    print("\n✅ Datos Cargados")

    print("\n🎯Tamaño del DataFrame:")
    print(df.shape)

    print("\n🎯Primeras filas del DataFrame:")
    print(df.head())

    return df

def save_data_preprocess(df: pd.DataFrame, scaler):
    """Guarda el dataset procesado en un archivo CSV."""
    file_path = os.path.join(LOCAL_DATA_PATH, FILE_DATA_PREPROCESS)
    file_path_scaler = os.path.join(LOCAL_MODELS_PATH, 'scaler.pkl')
    df.to_csv(file_path, index=False)
    joblib.dump(scaler, file_path_scaler)
    print("\n✅ Preprocesamiento guardado")

def load_data_preprocess() -> pd.DataFrame:
    """
    Obtener la data preprocesada
    """
    file_path = os.path.join(LOCAL_DATA_PATH, FILE_DATA_PREPROCESS)
    df = pd.read_csv(file_path)
    try:
        file_path_scaler = os.path.join(LOCAL_MODELS_PATH, 'scaler.pkl')
        scaler = joblib.load(file_path_scaler)
    except FileNotFoundError:
        scaler = None

    print("\n✅ Datos Preprocesados Cargados")

    return df, scaler
