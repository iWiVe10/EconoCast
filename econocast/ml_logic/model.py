import pandas as pd
import numpy as np
from econocast.params import *
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def build_model(df_preprocess):
    """Contruncion del modelo"""
    print("\n⌛ Construyendo modelo")

    # Definir variables independientes (exógenas) y la variable objetivo
    exogenous_vars = EXOGENOUS
    target_var = TARGET

    df_model = df_preprocess.dropna(subset=[target_var])  # Eliminar filas con NaN en el target

    # Definir datos de entrenamiento
    y = df_model.set_index("Fecha")[target_var]  # Establecer la fecha como índice
    X = df_model.set_index("Fecha")[exogenous_vars]  # Establecer la fecha como índice en X también

    # Definir datos de entrenamiento
    # y = df_model[target_var]
    # X = df_model[exogenous_vars]

    y = y.astype(float)
    X = X.replace({',': ''}, regex=True).astype(float)

    print("\n✅ Modelo construido")

    return X, y



def train_model(df_preprocess):
    """Entrena un modelo con redes neuronales."""
    # Construir modelo
    X, y = build_model(df_preprocess)

    print("\n⌛ Entrenando modelo")
    # Ajustar el modelo SARIMAX (ARIMA con variables exógenas)
    model_arimax = SARIMAX(y, exog=X, order=(0,1,2), seasonal_order=(2,0,2,12), enforce_stationarity=False, enforce_invertibility=False)
    model_arimax_fit = model_arimax.fit(disp=False)

    print("\n✅ Modelo entrenado")

        # Predicciones en el mismo conjunto de entrenamiento
    y_pred = model_arimax_fit.fittedvalues  # Predicciones del modelo en los datos de entrenamiento

    # Calcular métricas
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)

    print("\n📊 Evaluación del Modelo SARIMAX")
    print(f"🔹 MAE  (Error Absoluto Medio): {mae:.4f}")
    print(f"🔹 MSE  (Error Cuadrático Medio): {mse:.4f}")
    print(f"🔹 RMSE (Raíz del Error Cuadrático Medio): {rmse:.4f}")
    print(f"🔹 R² Score: {r2:.4f}")

    # Mostrar resumen del modelo
    print("\n📌 Resumen del modelo:")
    print(model_arimax_fit.summary())


    return model_arimax_fit



def predict_model(model, steps):
    """Genera predicciones con el modelo entrenado."""
    print("\n⌛ Prediciendo valor")

    # Realizar predicción para los próximos meses
    forecast_steps = steps
    ultima_fecha = pd.to_datetime(model.model.data.orig_endog.index.max())  # Asegura que es una fecha
    future_dates = pd.date_range(start=ultima_fecha, periods=forecast_steps+1, freq="MS")[1:]

    # Repetir las últimas observaciones de las variables exógenas para el período futuro
    X_last = model.model.exog[-1, :]
    X_future = pd.DataFrame(np.tile(X_last, (forecast_steps, 1)), columns=EXOGENOUS)

    # Predicción de inflación mensual con ARIMAX
    forecast_arimax = model.forecast(steps=forecast_steps, exog=X_future)

    # Crear un DataFrame con los resultados
    df_forecast_arimax = pd.DataFrame({"Fecha": future_dates, "Prediccion_inflacion_mensual": forecast_arimax})

    print(df_forecast_arimax.head())

    json_forecast = df_forecast_arimax.to_json(orient="records", date_format="iso")

    print("\n✅ Predicción realizada")

    return json_forecast
