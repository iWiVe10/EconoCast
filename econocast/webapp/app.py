import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# Configurar el diseño de la página para ser responsive
st.set_page_config(layout="wide")

weights = [31.81, 0.36, 8.17, 19.25, 6.67, 3.65, 9.05, 1.69, 3.97, 3.05, 7.15, 5.18]


# Mapeo de iconos para cada categoría
iconos_categorias = {
    "alimentos_bebidas_sin_alcohol": "🍎",
    "bebidas_alcoholicas_tabaco": "🍷",
    "prendas_de_vestir_calzado": "👕",
    "alojamiento_agua_electricidad_gas_otroscomb": "🏠",
    "muebles_articulos_hogar": "🛋️",
    "salud": "🏥",
    "transporte": "🚗",
    "comunicaciones": "📞",
    "recreacion_cultura": "🎭",
    "educacion": "📚",
    "restaurantes_hoteles": "🍽️",
    "cuidado_personal": "💆"
}

# Sidebar - Logo y selección de tipo de gasto en la parte gris
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.markdown("## Selección de tipo de gasto")
    categorias = list(iconos_categorias.keys())

    categorias_seleccionadas = st.multiselect("Selecciona los tipos de gasto", categorias, default=["transporte"])
    gastos_reales = {}
    for categoria in categorias_seleccionadas:
        gastos_reales[categoria] = st.number_input(f"¿Cuál es tu gasto mensual en {categoria}?", min_value=0.0, value=100.0)

    meses_a_proyectar = st.slider("¿Cuántos meses quieres proyectar?", min_value=1, max_value=12, value=6)

    if st.button("Predecir"):
        st.session_state["predicted"] = True

        # Obtener la fecha y hora actual
        fecha_actual = datetime.now()
        fecha_referencia = datetime(2025, 1, 1)
        diferencia_meses = (fecha_referencia.month - fecha_actual.month)

        response = requests.get(f'http://127.0.0.1:8000/predict/?steps={meses_a_proyectar + abs(diferencia_meses)}')

        data_inflacion = response.json()

        # Crear el DataFrame con los datos de inflación
        df_inflacion = pd.read_json(data_inflacion)

        fecha_inicial = datetime(2025, 2, 1)

        # Calcular el nuevo mes y año
        nuevo_mes = fecha_inicial.month + abs(diferencia_meses)
        nuevo_año = fecha_inicial.year

        # Ajustar el año y el mes si el mes supera 12
        if nuevo_mes > 12:
            # Calcular cuántos años hay que sumar
            años_a_sumar = (nuevo_mes - 1) // 12  # Esto da los años completos a sumar
            nuevo_mes = nuevo_mes % 12  # Calcula el mes restante
            if nuevo_mes == 0:  # Si el mes resulta en 0, ajustamos a diciembre
                nuevo_mes = 12
                años_a_sumar -= 1
            nuevo_año += años_a_sumar  # Sumar los años calculados

        # Crear la nueva fecha
        fecha_final = datetime(nuevo_año, nuevo_mes, 1)

        # Crear el DataFrame de predicción ajustado
        data = {"Fecha": pd.date_range(start=fecha_final, periods=meses_a_proyectar, freq="MS")}

        # Filtrar el DataFrame para que solo contenga las fechas a partir del mes actual
        df_inflacion['Fecha'] = pd.to_datetime(df_inflacion['Fecha'])


        df_inflacion = df_inflacion.iloc[abs(diferencia_meses):].reset_index(drop=True)


        for i, categoria in enumerate(iconos_categorias.keys()):
            # Obtener la predicción de inflación para la categoría y ajustarla según el peso
            prediccion_mensual = df_inflacion['Prediccion_inflacion_mensual'].iloc[:meses_a_proyectar]  # Ajusta según los datos de la API
            predicciones_ajustadas = prediccion_mensual * (weights[i] / 100)  # Aplicar el peso

            if categoria in gastos_reales:
                # Inicializar una lista para las predicciones ajustadas
                predicciones_finales = []

                # Primer mes: usar el gasto real como base
                gasto_anterior = gastos_reales[categoria] * (1 + (predicciones_ajustadas.iloc[0]/100))
                predicciones_finales.append(gasto_anterior)

                # Para los meses siguientes, aplicar la inflación sobre el valor del mes anterior
                for j in range(1, meses_a_proyectar):
                    gasto_anterior *= (1 + predicciones_ajustadas.iloc[j-1] / 100)  # Aplicar inflación sobre el valor del mes anterior
                    predicciones_finales.append(gasto_anterior)

                # Añadir las predicciones ajustadas al diccionario 'data'
                data[f"Predicción {categoria}"] = predicciones_finales

            # if categoria in gastos_reales:
            #     data[f"Predicción {categoria}"] = gastos_reales[categoria] * (1 + (predicciones_ajustadas/100))

        # Convertir el diccionario a DataFrame
        df = pd.DataFrame(data)

        st.session_state["data_inflacion_ajustada"] = df
        df["Fecha"] = df["Fecha"].dt.strftime("%Y-%m")

# Crear pestañas
st.markdown("""<style>
div[data-testid="stTabs"] > div {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
</style>""", unsafe_allow_html=True)
tabs = st.tabs(["General", "Análisis de Gastos"])

with tabs[1]:
    st.markdown("")

    if "predicted" in st.session_state:
        for categoria in categorias_seleccionadas:
            prediccion = df[f"Predicción {categoria}"].iloc[:meses_a_proyectar].mean()
            cambio = (prediccion - gastos_reales[categoria]) / gastos_reales[categoria] * 100
            color = "red" if cambio > 0 else "green"
            title_background = "#f8d7da" if cambio > 0 else "#d4edda"
            icono = iconos_categorias.get(categoria, "💰")

            st.markdown(
                f"""
                <div style="border-radius: 10px; padding: 10px; background-color: #ffffff; margin-bottom: 10px; width: 100%; max-width: 350px; text-align: center; border: 1px solid #ddd;">
                    <div style="background-color: {title_background}; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px; font-weight: bold;">
                        {icono} {categoria.replace('_', ' ').capitalize()}
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px;">
                        <div>
                            <b style="font-size: 14px;">${gastos_reales[categoria]:.2f}</b><br>
                            <span style="font-size: 12px;">LP</span>
                        </div>
                        <div>
                            <span style="color: {color}; font-size: 14px; font-weight: bold;">{cambio:.2f}% Cambio</span>
                        </div>
                        <div>
                            <b style="font-size: 14px;">${prediccion:.2f}</b><br>
                            <span style="font-size: 12px;">Predicción</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True
            )

with tabs[0]:
    if "predicted" in st.session_state:
        st.markdown("## Visualizacion")
        col1, col2 = st.columns(2)
        with col1:
            # Filtrar los valores de gastos_reales según las categorías seleccionadas
            gastos_seleccionados = [gastos_reales[c] for c in categorias_seleccionadas]

            # Calcular la suma total de los gastos seleccionados
            total_gastos = sum(gastos_seleccionados)

            # Calcular los porcentajes de cada valor seleccionado
            porcentajes_gastos = [gasto / total_gastos * 100 for gasto in gastos_seleccionados]

            # Crear el gráfico de pastel con los porcentajes
            fig_pie_real = go.Figure(data=[go.Pie(labels=gastos_seleccionados, values=porcentajes_gastos)])

            # Agregar título al gráfico
            fig_pie_real.update_layout(
                title="Distribución de los Gastos Seleccionados en %",
                title_x=0.5  # Centrar el título
            )

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig_pie_real, use_container_width=True)

        with col2:
            fig_pie_pred = px.pie(names=categorias_seleccionadas, values=[df[f"Predicción {c}"].iloc[:meses_a_proyectar].mean() for c in categorias_seleccionadas], title="Predicción de distribución de gastos")
            st.plotly_chart(fig_pie_pred, use_container_width=True)

        # Asegurar que df_comparacion contenga todas las categorías seleccionadas
        df_comparacion = df.iloc[:meses_a_proyectar][["Fecha"]].copy()

        for categoria in categorias_seleccionadas:
            df_comparacion[f"Predicción {categoria}"] = df[f"Predicción {categoria}"].iloc[:meses_a_proyectar]
            df_comparacion[f"Gasto Real {categoria}"] = gastos_reales[categoria]

        df_melted = df_comparacion.melt(id_vars=["Fecha"], var_name="variable", value_name="Monto")
        df_melted_pred = df_melted[df_melted["variable"].str.startswith("Predicción")]


        # Crear gráfico de líneas solo con predicciones
        fig_line = px.line(
            df_melted_pred,
            x="Fecha",
            y="Monto",
            color="variable",
            title="Predicción de Gastos",
            markers=True,
            line_shape="spline"
        )


        # Ajustar ancho de línea y mejorar visualización
        fig_line.update_traces(line=dict(width=3))
        fig_line.update_layout(
            xaxis_title="Fecha",
            yaxis_title="Monto",
            showlegend=True,
            template="plotly_white"
        )

        # Mostrar gráfico corregido
        st.plotly_chart(fig_line, use_container_width=True)


        df_filtered = df.iloc[:meses_a_proyectar][["Fecha"] + [f"Predicción {c}" for c in categorias_seleccionadas]]
        for c in categorias_seleccionadas:
            df_filtered[f"Diferencia {c}"] = df_filtered[f"Predicción {c}"] - gastos_reales[c]

        def highlight(val):
            return f'color: {"red" if val > 0 else "green"}'

        st.dataframe(df_filtered.style.applymap(highlight, subset=[f"Diferencia {c}" for c in categorias_seleccionadas]))

        st.download_button("Descargar CSV", df_filtered.to_csv(index=False).encode("utf-8"), "prediccion_gastos.csv", "text/csv")
