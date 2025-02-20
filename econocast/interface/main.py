import pandas as pd
import numpy as np
from econocast.ml_logic.data import load_data, save_data_preprocess, load_data_preprocess
from econocast.ml_logic.preprocessor import preprocess_data, clean_data
from econocast.ml_logic.model import train_model, evaluate_model, predict_model, create_sequences
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
    df_scaled, scaler = preprocess_data(df)

    # Guarda el procesamiento
    save_data_preprocess(df_scaled, scaler)

    print("\n✅📦 Preprocesamiento completado y guardado")

    return df_scaled, scaler

# ===============================
# Entrenamiento del Modelo
# ===============================
def train():
    """Entrena un modelo de ARIMA para series temporales."""
    print("\n🚀⭐️ Iniciando Entrenamiento")

    # Cargando data preprocesada
    df_scaled, scaler = load_data_preprocess()

    # Creando secuencia
    X, y = create_sequences(df_scaled, seq_length=18)

    train_size = int(len(X) * 0.8)
    X_train, X_test, y_train, y_test = X[:train_size], X[train_size:], y[:train_size], y[train_size:]

    # Entrenando modelo
    model = train_model(X_train, y_train, X_test, y_test)

    # Guardando modelo entrenado
    model_name = 'RNN_model'
    save_model(model, scaler, model_name)

    print("✅📦 Modelo entrenado y guardado")

    return model


# ===============================
# Evaluación del Modelo
# ===============================
def evaluate():
    """Evalúa el modelo ARIMA entrenado con datos de validación."""
    print("\n📊⭐️ Iniciando Evaluacion")
    # Cargar modelo
    model, _ = load_model('RNN_model')

    # Cargar data escalada
    df_scaled, scaler = load_data_preprocess()

    # Crear secuencia
    X, y = create_sequences(df_scaled, seq_length=18)

    train_size = int(len(X) * 0.8)
    X_test, y_test = X[train_size:], y[train_size:]

    loss, mae, mse = evaluate_model(model, X_test, y_test )

    # Mostrar resultados
    print(f"\n✅📉 Evaluación completada.")
    print(f"📌 LOSS  (Perdida): {loss:.4f}")
    print(f"📌 MAE  (Error Absoluto Medio): {mae:.4f}")
    print(f"📌 RMSE (Error Cuadrático Medio): {mse:.4f}")

    return loss, mae, mse



# ===============================
# Predicción con ARIMA
# ===============================
def pred():
    """
    Genera predicciones usando el modelo ARIMA entrenado.
    """

    print("\n⭐️ Iniciando prediccion")

    model, _ = load_model('RNN_model')
    df_scaled, escalado = load_data_preprocess()
    sample = df_scaled.iloc[-18:].values.reshape(1, 18, -1)
    prediction = predict_model(model, sample)
    print(f"🔹 Predicción Normalizada: {prediction[0][0]}")  # Depuración
    if _:
        descaled_prediction = _.inverse_transform(np.array(prediction).reshape(-1, 1))[0, 0]
        print(f"🔹 Predicción Desescalada: {descaled_prediction}")  # Depuración

        return {"valor": float(descaled_prediction)}
    return {"valor": float(prediction[0][0])}



if __name__ == '__main__':
    preprocess()
    train()
    evaluate()
    pred()
