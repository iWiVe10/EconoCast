
from econocast.ml_logic.data import load_data, save_data_preprocess, load_data_preprocess
from econocast.ml_logic.preprocessor import preprocess_data, clean_data
from econocast.ml_logic.model import train_model, predict_model
from econocast.ml_logic.registry import save_model, load_model
from econocast.params import *

# ===============================
# Preprocesamiento de Datos
# ===============================
def preprocess():
    """Carga y preprocesa el dataset."""
    print("\n🚀⭐️ Iniciando Preprocesamiento de Datos")

    # Cargar data cruda
    df = load_data()

    # Limpieza de data (no estaba antes)
    df = clean_data(df)

    # Preprocesamiento de data
    df_preprocess = preprocess_data(df)

    # Guarda el procesamiento
    save_data_preprocess(df_preprocess)

    print("\n✅📦 Preprocesamiento completado y guardado")


# ===============================
# Entrenamiento del Modelo
# ===============================
def train():
    """Entrena un modelo de SARIMAX para series temporales."""
    print("\n🚀⭐️ Iniciando Entrenamiento")

    # Cargando data preprocesada
    df_preprocess = load_data_preprocess()

    # Entrenando modelo
    model_entrenado = train_model(df_preprocess)

    # Guardando modelo entrenado
    model_name = 'SARIMAX_model'
    save_model(model_entrenado, model_name)

    print("\n✅📦 Modelo entrenado y guardado")

    return model_entrenado


# ===============================
# Predicción con SARIMAX
# ===============================
def pred(steps: int):
    """
    Genera predicciones usando el modelo SARIMAX entrenado.
    """

    print("\n⭐️ Iniciando prediccion")

    model = load_model('SARIMAX_model')

    response = predict_model(model, steps)

    print("\n✅ Predicciones listas")

    return response




if __name__ == '__main__':
    preprocess()
    train()
    pred()
