import tensorflow as tf
import numpy as np
from econocast.params import *


def build_model(input_shape):
    """Contruncion del modelo"""
    print("\n⌛ Construyendo modelo")
    model = tf.keras.models.Sequential([
         tf.keras.layers.LSTM(50, return_sequences=True, input_shape=input_shape),
         tf.keras.layers.Dropout(0.2),
         tf.keras.layers.LSTM(50),
         tf.keras.layers.Dropout(0.2),
         tf.keras.layers.Dense(1, activation='linear')
    ])

    print("\n✅ Modelo construido")

    print("\n⌛ Compilando modelo")
    model.compile(optimizer='adam', loss='mse', metrics=['mae', 'mse'])
    print("\n✅ Modelo compilado: adam y mse")

    return model

def create_sequences(df_scaled, seq_length=18):
    """Creacion de secuencia"""
    print(f'\n⌛ Creando secuencias de {seq_length} meses')
    X, y = [], []
    for i in range(len(df_scaled) - seq_length):
        X.append(df_scaled.iloc[i:i+seq_length].values)
        y.append(df_scaled.iloc[i+seq_length][TARGET])

    print("\n✅ Secuencias creadas")
    return np.array(X), np.array(y)

def train_model(X_train, y_train, X_test, y_test):
    """Entrena un modelo con redes neuronales."""
    model = build_model((X_train.shape[1], X_train.shape[2]))

    print("\n⌛ Entrenando modelo")
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test), callbacks=[early_stopping])
    print("\n✅ Modelo entrenado")

    return model

def evaluate_model(model, X_test, y_test):
    """Evalúa el modelo."""
    print("\n⌛ Evaluando modelo")
    loss, mae, mse = model.evaluate(X_test, y_test, verbose=1)
    print("\n✅ Modelo evaluado")

    return loss, mae, mse

def predict_model(model, input_data):
    """Genera predicciones con el modelo entrenado."""
    print("\n⌛ Prediciendo valor")
    response = model.predict(input_data)
    print("\n✅ Prediccion realizada")
    print(response)
    return response
