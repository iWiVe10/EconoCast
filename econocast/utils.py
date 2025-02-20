import pandas as pd
from statsmodels.tsa.stattools import adfuller
from econocast.params import *

def check_stationarity(df: pd.DataFrame):
    """Verifica la estacionaridad con la prueba ADF y aplica múltiples diferenciaciones si es necesario."""
    print("\n📉⭐️ Checking Stationarity")
    d = 0

    while True:
        result = adfuller(df[TARGET].dropna())
        print(f"📉 ADF Statistic: {result[0]}")
        print(f"p-value: {result[1]}")
        print("Critical Values:")
        for key, value in result[4].items():
            print(f"\t{key}: {value}")

        if result[1] < 0.05:
            print(f"✅ La serie es ESTACIONARIA con d={d} (p-value < 0.05)")
            break
        else:
            print(f"⚠ La serie NO es estacionaria (p-value >= 0.05), aplicando diferenciación d={d+1}.")
            df[TARGET] = df[TARGET].diff().dropna()
            d += 1
            if d > 2:
                print("❌ Advertencia: Se alcanzó d=2 y la serie sigue sin ser estacionaria.")
                break

    return df, d
