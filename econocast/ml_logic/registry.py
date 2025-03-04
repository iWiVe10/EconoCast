import os
import pickle
from econocast.params import *


def save_model(model, name_model):
    """Guarda el modelo entrenado en un archivo."""
    file_path = os.path.join(LOCAL_MODELS_PATH, f'{name_model}.pkl')
    with open(file_path, "wb") as f:
        pickle.dump(model, f)
    print("\n✅ Modelo Guardado")


def load_model(name_model):
    """Carga un modelo previamente guardado."""
    file_path = os.path.join(LOCAL_MODELS_PATH, f"{name_model}.pkl")
    with open(file_path, "rb") as f:
        model = pickle.load(f)
    print("\n✅ Modelo SARIMAX Cargado")
    return model
