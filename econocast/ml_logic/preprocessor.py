import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza y transformación inicial del dataset"""
    print("\n⌛ Limpiando datos")

    df["Fecha"] = pd.to_datetime(df["anio"].astype(str) + "-" + df["mes"], format="%Y-%B", errors="coerce")# Diccionario de nombres de meses en español a números
    meses_dict = {
        "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04",
        "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08",
        "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
    }

    # Reemplazar los nombres de los meses por su número correspondiente
    df["mes"] = df["mes"].replace(meses_dict)

    # Crear la columna de fecha correctamente en formato YYYY-MM
    df["Fecha"] = pd.to_datetime(df["anio"].astype(str) + "-" + df["mes"], format="%Y-%m", errors="coerce")

    df_filtered = df[["Fecha", "indice_ipc_general", "precio_promedio_venta_USD",
                            "promedio_valor_USD_anual", "importaciones_valor_usd",
                            "importaciones_volumen_kg", "exportaciones_valor_usd",
                            "exportaciones_volumen_kg", "alimentos_bebidas_sin_alcohol",
                            "bebidas_alcoholicas_tabaco", "prendas_de_vestir_calzado",
                            "alojamiento_agua_electricidad_gas_otroscomb",
                            "muebles_articulos_hogar", "salud", "transporte", "comunicaciones",
                            "recreacion _cultura", "educacion", "restaurantes_hoteles",
                            "cuidado_personal"]].copy()

    df_filtered = df_filtered.sort_values(by="Fecha").reset_index(drop=True)

    # Rellenar valores faltantes
    df_filtered = df_filtered.fillna(method="ffill")
    df_filtered = df_filtered.fillna(method="bfill")


    print("\n✅ Datos limpios")
    return df_filtered

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n⌛ Agregando Features de inflacion")

    # Calcular la inflación mensual e interanual
    df["Inflación Mensual (%)"] = df["indice_ipc_general"].pct_change() * 100
    df["Inflación Interanual (%)"] = df["indice_ipc_general"].pct_change(periods=12) * 100

    # alimentos_bebidas_sin_alcohol
    df["alimentos_bebidas_sin_alcohol M(%)"] = df["alimentos_bebidas_sin_alcohol"].pct_change() * 100
    df["alimentos_bebidas_sin_alcohol I(%)"] = df["alimentos_bebidas_sin_alcohol"].pct_change(periods=12) * 100

    # bebidas_alcoholicas_tabaco
    df["bebidas_alcoholicas_tabaco M(%)"] = df["bebidas_alcoholicas_tabaco"].pct_change() * 100
    df["bebidas_alcoholicas_tabaco I(%)"] = df["bebidas_alcoholicas_tabaco"].pct_change(periods=12) * 100

    # prendas_de_vestir_calzado
    df["prendas_de_vestir_calzado M(%)"] = df["prendas_de_vestir_calzado"].pct_change() * 100
    df["prendas_de_vestir_calzado I(%)"] = df["prendas_de_vestir_calzado"].pct_change(periods=12) * 100

    # alojamiento_agua_electricidad_gas_otroscomb
    df["alojamiento_agua_electricidad_gas_otroscomb M(%)"] = df["alojamiento_agua_electricidad_gas_otroscomb"].pct_change() * 100
    df["alojamiento_agua_electricidad_gas_otroscomb I(%)"] = df["alojamiento_agua_electricidad_gas_otroscomb"].pct_change(periods=12) * 100

    # muebles_articulos_hogar
    df["muebles_articulos_hogar M(%)"] = df["muebles_articulos_hogar"].pct_change() * 100
    df["muebles_articulos_hogar I(%)"] = df["muebles_articulos_hogar"].pct_change(periods=12) * 100

    # salud
    df["salud M(%)"] = df["salud"].pct_change() * 100
    df["salud I(%)"] = df["salud"].pct_change(periods=12) * 100

    # transporte
    df["transporte M(%)"] = df["transporte"].pct_change() * 100
    df["transporte I(%)"] = df["transporte"].pct_change(periods=12) * 100

    # comunicaciones
    df["comunicaciones M(%)"] = df["comunicaciones"].pct_change() * 100
    df["comunicaciones I(%)"] = df["comunicaciones"].pct_change(periods=12) * 100

    # recreacion _cultura
    df["recreacion _cultura M(%)"] = df["recreacion _cultura"].pct_change() * 100
    df["recreacion _cultura I(%)"] = df["recreacion _cultura"].pct_change(periods=12) * 100

    # educacion
    df["educacion M(%)"] = df["educacion"].pct_change() * 100
    df["educacion I(%)"] = df["educacion"].pct_change(periods=12) * 100

    # restaurantes_hoteles
    df["restaurantes_hoteles M(%)"] = df["restaurantes_hoteles"].pct_change() * 100
    df["restaurantes_hoteles I(%)"] = df["restaurantes_hoteles"].pct_change(periods=12) * 100

    # cuidado_personal
    df["cuidado_personal M(%)"] = df["cuidado_personal"].pct_change() * 100
    df["cuidado_personal I(%)"] = df["cuidado_personal"].pct_change(periods=12) * 100

    # Rellenar valores faltantes
    df = df.fillna(method="ffill")
    df = df.fillna(method="bfill")

    print("\n🎯Primeras filas del DataFrame Preprocesado:")
    print(df.head())

    print("\n🎯Ultimas filas del DataFrame Preprocesado:")
    print(df.tail())

    print("\n✅ Features agregadas correctamente")
    return df
