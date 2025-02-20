import joblib
from econocast.params import *
import tensorflow as tf

def save_model(model, scaler, name_model):
    """Guarda el modelo entrenado en un archivo."""
    file_path = os.path.join(LOCAL_MODELS_PATH, name_model)
    model.save(f'{file_path}.h5')
    print("\n✅ Modelo Guardado")


def load_model(name_model):
    """Carga un modelo previamente guardado."""
    file_path = os.path.join(LOCAL_MODELS_PATH, name_model)
    file_path_scaler = os.path.join(LOCAL_MODELS_PATH, 'scaler.pkl')
    model = tf.keras.models.load_model(f'{file_path}.h5')
    scaler = joblib.load(file_path_scaler)
    print(f"📏 Min IPC: {scaler.data_min_[0]}, Max IPC: {scaler.data_max_[0]}")


    print("\n✅ Modelo Cargado")
    return model, scaler
