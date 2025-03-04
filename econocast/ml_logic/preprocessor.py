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
                            "exportaciones_volumen_kg"]].copy()

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

    print("\n🎯Primeras filas del DataFrame Preprocesado:")
    print(df.head())

    print("\n🎯Ultimas filas del DataFrame Preprocesado:")
    print(df.tail())

    print("\n✅ Features agregadas correctamente")
    return df
