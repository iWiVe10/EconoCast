import os
import numpy as np

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LOCAL_DATA_PATH = os.path.join(parent_directory, "data")
LOCAL_MODELS_PATH =  os.path.join(parent_directory, "models")

FILE_DATA = 'raw_Data_Econocast.csv'
FILE_DATA_PREPROCESS = 'preprocess_Data_Econocast.csv'

TARGET = "Inflación Mensual (%)"

EXOGENOUS = ['precio_promedio_venta_USD', 'promedio_valor_USD_anual',
       'importaciones_valor_usd',
       'importaciones_volumen_kg', 'exportaciones_valor_usd',
       'exportaciones_volumen_kg', 'Inflación Interanual (%)',
       'alimentos_bebidas_sin_alcohol M(%)',
       'alimentos_bebidas_sin_alcohol I(%)', 'bebidas_alcoholicas_tabaco M(%)',
       'bebidas_alcoholicas_tabaco I(%)', 'prendas_de_vestir_calzado M(%)',
       'prendas_de_vestir_calzado I(%)',
       'alojamiento_agua_electricidad_gas_otroscomb M(%)',
       'alojamiento_agua_electricidad_gas_otroscomb I(%)',
       'muebles_articulos_hogar M(%)', 'muebles_articulos_hogar I(%)',
       'salud M(%)', 'salud I(%)', 'transporte M(%)', 'transporte I(%)',
       'comunicaciones M(%)', 'comunicaciones I(%)',
       'recreacion _cultura M(%)', 'recreacion _cultura I(%)',
       'educacion M(%)', 'educacion I(%)', 'restaurantes_hoteles M(%)',
       'restaurantes_hoteles I(%)', 'cuidado_personal M(%)',
       'cuidado_personal I(%)']
