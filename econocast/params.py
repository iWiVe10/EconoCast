import os
import numpy as np

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LOCAL_DATA_PATH = os.path.join(parent_directory, "data")
LOCAL_MODELS_PATH =  os.path.join(parent_directory, "models")

FILE_DATA = 'raw_Data_Econocast.csv'
FILE_DATA_PREPROCESS = 'preprocess_Data_Econocast.csv'

TARGET = "Inflación Mensual (%)"

EXOGENOUS = ["precio_promedio_venta_USD", "promedio_valor_USD_anual",
                    "importaciones_valor_usd", "importaciones_volumen_kg",
                    "exportaciones_valor_usd", "exportaciones_volumen_kg"]
