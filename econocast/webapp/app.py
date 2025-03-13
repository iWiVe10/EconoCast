import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import base64


# Configurar el diseño de la página para ser responsive
st.set_page_config(layout="wide", page_title="FinTrack - Bienvenidos", page_icon=":chart_with_upwards_trend:")

# Función para cargar imágenes y convertirlas a base64
def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Convertir las imágenes a base64
logo_base64 = get_image_as_base64("logo.png")
welcome_image_base64 = get_image_as_base64("ecomics.jpg")

# Definir el estado inicial
if "show_welcome" not in st.session_state:
    st.session_state["show_welcome"] = True

# Agregar estilos sin modificar el código de la lógica
st.markdown(
    """
    <style>
        .welcome-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .welcome-text {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .welcome-title {
            font-size: 40px;
            font-weight: bold;
            color: #4A4A8A;
            margin-bottom: 10px;
        }
        .welcome-subtitle {
            font-size: 22px;
            color: #FFC107;
            margin-bottom: 20px;
        }
        .welcome-description {
            font-size: 18px;
            color: #6C757D;
            max-width: 600px;
            margin-bottom: 20px;
        }
        .welcome-button {
            background-color: #6C63FF;
            color: white;
            padding: 12px 25px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            transition: 0.3s;
        }
        .welcome-button:hover {
            background-color: #5145CD;
        }
        .welcome-image {
            max-width: 500px;
            border-radius: 15px;
            box-shadow: 5px 5px 20px rgba(0,0,0,0.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Página de presentación
if st.session_state["show_welcome"]:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="welcome-text">', unsafe_allow_html=True)
        st.image(f"data:image/png;base64,{logo_base64}", width=150)
        st.markdown("<h1 class='welcome-title'>¡BIENVENIDO A FINTRACK!</h1>", unsafe_allow_html=True)
        st.markdown("<h3 class='welcome-subtitle'>Planifica tu futuro financiero</h3>", unsafe_allow_html=True)
        st.markdown("<p class='welcome-description'>FinTrack es una herramienta avanzada que predice la inflación a *N* meses y te ayuda a anticiparte "
                    "a los cambios en la economía. Aplicamos los índices de inflación a tus gastos personales para que conozcas "
                    "cómo afectará la economía a tu bolsillo. ¿Tus gastos subirán o bajarán? ¡Descúbrelo ahora!</p>",
                    unsafe_allow_html=True)

        if st.button("Comenzar Análisis", key="start_analysis"):
            st.session_state["show_welcome"] = False
            st.experimental_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="welcome-text">', unsafe_allow_html=True)
        st.image(f"data:image/png;base64,{welcome_image_base64}", width=700)
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()



# Reducir el margen superior con CSS
st.markdown("""
    <style>
        div.block-container {padding-top: 10px !important;}

        /* Estilos para los números en las instrucciones */
        .instruction-list {
            list-style: none;
            padding-left: 0;
        }

        .instruction-list li {
            display: flex;
            align-items: center;
            font-size: 16px;
            margin-bottom: 10px;
        }

        .instruction-number {
            width: 25px;
            height: 25px;
            background-color: red;
            color: white;
            font-weight: bold;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

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

webApp_categorias = {
    "alimentos_bebidas_sin_alcohol": "Alimentos, bebidas sin alcohol",
    "bebidas_alcoholicas_tabaco": "Bebidas alcoholicas, tabaco",
    "prendas_de_vestir_calzado": "Prendas de vestir calzado",
    "alojamiento_agua_electricidad_gas_otroscomb": "Alojamiento, agua, electricidad, gas, otros...",
    "muebles_articulos_hogar": "Muebles, articulos de hogar",
    "salud": "Salud",
    "transporte": "Transporte",
    "comunicaciones": "Comunicaciones",
    "recreacion_cultura": "Recreación, cultura",
    "educacion": "Educación",
    "restaurantes_hoteles": "Restaurantes, hoteles",
    "cuidado_personal": "Cuidado personal"
}

# Definir función para resetear predicción
def reset_prediction():
    if "predicted" in st.session_state:
        st.session_state["predicted"] = False

# Sidebar - Logo y selección de tipo de gasto en la parte gris
with st.sidebar:
    st.image("./logo.png", width=140)
    st.markdown("## Selección de tipo de gasto")

    # Crear el mapeo entre nombres visibles y claves internas
    categorias_visibles = list(webApp_categorias.values())
    mapa_inverso = {v: k for k, v in webApp_categorias.items()}  # Para recuperar la clave desde el valor

    # Multiselect con valores visibles pero trabajando con las claves internas
    categorias_seleccionadas_visibles = st.multiselect(
        "Selecciona los tipos de gasto", categorias_visibles,
        on_change=reset_prediction
    )

    # Convertir las selecciones visibles a claves internas
    categorias_seleccionadas = [mapa_inverso[cat] for cat in categorias_seleccionadas_visibles]

    # Capturar los gastos con las claves internas
    gastos_reales = {}
    for categoria in categorias_seleccionadas:
        gastos_reales[webApp_categorias[categoria]] = st.number_input(
            f"¿Cuál es tu gasto mensual en {webApp_categorias[categoria]}?", min_value=0, value=1,
            on_change=reset_prediction
        )

    meses_a_proyectar = st.slider("¿Cuántos meses quieres proyectar?", min_value=1, max_value=36, value=1,
                                  on_change=reset_prediction)

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


        for i, categoria in enumerate(webApp_categorias.values()):
            # Obtener la Predicción para inflación para la categoría y ajustarla según el peso
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
                data[f"Predicción para {categoria}"] = predicciones_finales

            # if categoria in gastos_reales:
            #     data[f"Predicción {categoria}"] = gastos_reales[categoria] * (1 + (predicciones_ajustadas/100))

        # Convertir el diccionario a DataFrame
        df = pd.DataFrame(data)
        st.session_state["data_inflacion_ajustada"] = df
        df["Fecha"] = df["Fecha"].dt.strftime("%Y-%m")

        df_filtered = df.iloc[:meses_a_proyectar][["Fecha"] + [f"Predicción para {webApp_categorias[c]}" for c in categorias_seleccionadas]]
        for c in categorias_seleccionadas:
            df_filtered[f"Diferencia de {webApp_categorias[c]}"] = df_filtered[f"Predicción para {webApp_categorias[c]}"] - gastos_reales[webApp_categorias[c]]

        st.session_state["data_inflacion_ajustada"] = df_filtered

# Instrucciones antes de predecir
if "predicted" not in st.session_state or not st.session_state["predicted"]:
    st.markdown("<h3 style='font-size: 30px;'>¡Descubre cómo la inflación afecta tu bolsillo!</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #6C757D; margin-top:0px;'>Anticípate a los cambios en la economía. Conoce cómo la inflación afectará tus gastos y ajusta tu presupuesto de manera inteligente.</p>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 24px;'>Instrucciones de uso</h3>", unsafe_allow_html=True)
    st.markdown("""
    <ul class="instruction-list">
        <li><span class="instruction-number">1</span>Selecciona los tipos de gasto en la barra lateral.</li>
        <li><span class="instruction-number">2</span>Ingresa el monto correspondiente a cada gasto.</li>
        <li><span class="instruction-number">3</span>Elige la cantidad de meses a proyectar.</li>
        <li><span class="instruction-number">4</span>Haz clic en  <b style="margin-left: 2px; margin-right: 2px;">Predecir</b>  para ver los resultados.</li>
    </ul>
    """, unsafe_allow_html=True)


if "predicted" in st.session_state and st.session_state["predicted"]:
    st.markdown("<h3 style='font-size: 30px;'>Dashboard de Predicción Financiera</h3>", unsafe_allow_html=True)

    # Crear pestañas
    st.markdown("""<style>
    div[data-testid="stTabs"] > div {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: -20px !important;  /* Eliminar margen superior */
        padding-top: 0px !important; /* Eliminar padding superior */
    }
    </style>""", unsafe_allow_html=True)
    tabs = st.tabs(["Resumen", "Tendencia", "Análisis de Gastos"])


    with tabs[0]:
        if "predicted" in st.session_state:
            # Agregar estilos para mejorar la interfaz
            st.markdown(
                """
                <style>
                    body {
                        font-family: 'Arial', sans-serif;
                        background-color: #f8f9fa;
                    }
                    .chart-container {
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                        margin-top: 20px;
                    }
                    .stTabs [data-baseweb="tab-list"] {
                        justify-content: start;
                    }
                    .info-box {
                        background-color: #f8f9fa;
                        padding: 15px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                        font-size: 16px;
                    }
                    .styled-table {
                        border-collapse: collapse;
                        width: 100%;
                        margin-top: 10px;
                    }
                    .styled-table th, .styled-table td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: center;
                    }
                    .styled-table th {
                        background-color: #f4f4f4;
                        font-weight: bold;
                    }
                    .increase { color: red; }
                    .decrease { color: green; }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<h3 style='font-size: 24px;'>Situación Actual vs Situación Proyectada</h3>", unsafe_allow_html=True)


            st.markdown("""
                <div class="info-box">
                    <b>📊 Distribución de Gastos Actuales:</b> Este gráfico representa cómo se distribuyen tus gastos actualmente.
                    Selecciona diferentes categorías para ver su impacto en tu presupuesto.
                </div>

                <div class="info-box">
                    <b>📊 Distribución Proyectada de Gastos:</b> Basado en la predicción de inflación, este gráfico muestra cómo podrían cambiar tus gastos en los próximos meses.
                </div>
                """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                # Filtrar los valores de gastos_reales según las categorías seleccionadas
                gastos_seleccionados = [gastos_reales[webApp_categorias[c]] for c in categorias_seleccionadas]

                # Calcular la suma total de los gastos seleccionados
                total_gastos = sum(gastos_seleccionados)

                # Calcular los porcentajes de cada valor seleccionado
                porcentajes_gastos = [gasto / total_gastos * 100 for gasto in gastos_seleccionados]

                # Crear diccionario con nombres correctos y sus valores porcentuales
                diccionario_pie = {webApp_categorias[c]: porcentajes_gastos[i] for i, c in enumerate(categorias_seleccionadas)}

                # Mostrar en el gráfico de pastel usando los nombres correctos
                fig_pie_real = go.Figure(data=[go.Pie(labels=list(diccionario_pie.keys()), values=list(diccionario_pie.values()))])


                # Agregar título al gráfico
                fig_pie_real.update_layout(
                    title={
                        "text": "Distribución de los Gastos Actuales en %",
                        "x": 0.5,  # Centra horizontalmente
                        "y": 0.95,  # Ajusta la posición verticalmente (más arriba)
                        "xanchor": "center",
                        "yanchor": "top"
                    }
                )

                # Mostrar el gráfico en Streamlit
                st.plotly_chart(fig_pie_real, use_container_width=True)

            with col2:
                # Obtener el último registro del DataFrame df_filtered
                ultimo_registro = df_filtered.iloc[-1]

                # Extraer los valores de predicción del último mes
                predicciones_ultimo_mes = [ultimo_registro[f"Predicción para {webApp_categorias[c]}"] for c in categorias_seleccionadas]

                # Calcular la suma total de las predicciones del último mes
                total_predicciones = sum(predicciones_ultimo_mes)

                # Calcular los porcentajes de cada categoría en la predicción
                porcentajes_prediccion = [valor / total_predicciones * 100 for valor in predicciones_ultimo_mes] if total_predicciones > 0 else [0] * len(predicciones_ultimo_mes)

                # Crear diccionario con nombres correctos y sus valores porcentuales
                diccionario_pie_pred = {webApp_categorias[c]: porcentajes_prediccion[i] for i, c in enumerate(categorias_seleccionadas)}

                # Crear gráfico de pastel con valores del último mes
                fig_pie_pred = go.Figure(data=[go.Pie(labels=list(diccionario_pie_pred.keys()), values=list(diccionario_pie_pred.values()))])

                # Agregar título centrado
                fig_pie_pred.update_layout(
                    title={
                        "text": "Distribución Proyectada de los Gastos",
                        "x": 0.5,
                        "y": 0.95,
                        "xanchor": "center",
                        "yanchor": "top"
                    }
                )

                # Mostrar gráfico en Streamlit
                st.plotly_chart(fig_pie_pred, use_container_width=True)

    with tabs[1]:
        if "predicted" in st.session_state:
            st.markdown("<h3 style='font-size: 24px;'>Comportamiento de Inflación/Deflación en tus Gastos</h3>", unsafe_allow_html=True)


            st.markdown("""
                <div class="info-box">
                    <b>📉 Evolución de Predicciones de Gastos:</b> Este gráfico representa la tendencia de tus gastos a lo largo del tiempo con base en la inflación esperada.
                </div>
                """, unsafe_allow_html=True)

            df_filtered =  st.session_state["data_inflacion_ajustada"]

            # 🔹 Revisar valores únicos en las columnas de predicción
            columnas_prediccion = [col for col in df_filtered.columns if col.startswith("Diferencia de")]

            df_filtered["Fecha"] = pd.to_datetime(df_filtered["Fecha"], format="%Y-%m-%d", errors="coerce")

            for col in columnas_prediccion:
                df_filtered[col] = pd.to_numeric(df_filtered[col], errors="coerce")

            fig = go.Figure()

            for col in columnas_prediccion:
                fig.add_trace(go.Scatter(
                    x=df_filtered["Fecha"],
                    y=df_filtered[col].tolist(),  # Convertir a lista
                    mode="lines+markers",
                    name=col,
                    line=dict(width=2)
                ))

            # Calcular el rango del eje Y
            ymin = df_filtered[columnas_prediccion].min().min()
            ymax = df_filtered[columnas_prediccion].max().max()

            # Agregar un margen del 10%
            margen = 0.1 * (ymax - ymin)
            ymin -= margen
            ymax += margen

            fig.update_layout(
                title="Evolución de Predicciones de Gastos",
                xaxis_title="Fecha",
                yaxis_title="Diferencias en los Gastos",
                template="plotly_white",
                xaxis=dict(tickformat="%Y-%m", showgrid=True),
                yaxis=dict(tickformat=".2f", showgrid=True, autorange=False, range=[ymin, ymax])
            )

            st.plotly_chart(fig, use_container_width=True)



            st.markdown("""
            <div class="info-box">
                <b>📋 Resumen de Predicciones:</b> Esta tabla muestra cómo evolucionarán tus gastos en los próximos meses según la inflación esperada.
                Observa las diferencias y ajusta tu presupuesto.
            </div>
            """, unsafe_allow_html=True)

            #Mostra tabla
            def highlight(val):
                return f'color: {"red" if val > 0 else "green"}'

            st.dataframe(df_filtered.style.applymap(highlight, subset=[f"Diferencia de {webApp_categorias[c]}" for c in categorias_seleccionadas]))

            # # Obtener dinámicamente las columnas de predicción y diferencia
            # columnas_prediccion = [col for col in df_filtered.columns if "Predicción" in col]
            # columnas_diferencia = [col for col in df_filtered.columns if "Diferencia" in col]

            # # Función para dar formato con flechas en diferencias
            # def format_diff(val):
            #     arrow = "🔼" if val > 0 else "🔽"
            #     color = "red" if val > 0 else "green"
            #     return f'<span style="color: {color}; font-weight: bold;">{val:.2f} {arrow}</span>'


            # # Construcción de tabla con formato dinámico
            # st.markdown("<table class='styled-table'>", unsafe_allow_html=True)

            # # Construir encabezados de la tabla
            # encabezados = "<tr><th>Fecha</th>"
            # for pred, diff in zip(columnas_prediccion, columnas_diferencia):
            #     encabezados += f"<th>{pred}</th><th>{diff}</th>"
            # encabezados += "</tr>"

            # st.markdown(encabezados, unsafe_allow_html=True)

            # # Construir filas de datos dinámicamente
            # for i in range(len(df_filtered)):
            #     fila = f"<tr><td>{df_filtered.iloc[i]['Fecha']}</td>"
            #     for pred, diff in zip(columnas_prediccion, columnas_diferencia):
            #         fila += f"<td>{df_filtered.iloc[i][pred]:.2f}</td><td>{format_diff(df_filtered.iloc[i][diff])}</td>"
            #     fila += "</tr>"
            #     st.markdown(fila, unsafe_allow_html=True)

            # st.markdown("</table>", unsafe_allow_html=True)

            # # Botón de descarga
            # st.download_button("Descargar CSV", df_filtered.to_csv(index=False).encode("utf-8"), "prediccion_gastos.csv", "text/csv")



            st.download_button("Descargar CSV", df_filtered.to_csv(index=False).encode("utf-8"), "prediccion_gastos.csv", "text/csv")

    with tabs[2]:
        st.markdown("<h3 style='font-size: 24px;'>Variación Final de tus Gastos</h3>", unsafe_allow_html=True)


        st.markdown("""
            <div class="info-box">
                <b>📉 Análisis de Cambio en Gastos:</b>
                    Se muestra la comparación entre el gasto actual y la predicción futura
                    para la categoría seleccionada. También se destaca la tasa de variación
                    (% de cambio) esperada en función de los datos históricos.
            </div>
            """, unsafe_allow_html=True)

        if "predicted" in st.session_state:
            st.markdown(
                """
                <style>
                    .contenedor {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 15px;
                        justify-content: center;
                        align-items: flex-start;
                    }
                    .tarjeta {
                        border-radius: 10px;
                        padding: 10px;
                        background-color: #ffffff;
                        width: 320px;
                        text-align: center;
                        border: 1px solid #ddd;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                    }
                    .tarjeta-titulo {
                        padding: 10px;
                        font-weight: bold;
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                    }
                    .tarjeta-cuerpo {
                        display: flex;
                        justify-content: space-between;
                        padding: 10px;
                    }
                </style>
                <div class="contenedor">
                """, unsafe_allow_html=True
            )

            for categoria in categorias_seleccionadas:
                prediccion = df[f"Predicción para {webApp_categorias[categoria]}"].iloc[-1]
                cambio = (prediccion - gastos_reales[webApp_categorias[categoria]]) / gastos_reales[webApp_categorias[categoria]] * 100
                color = "red" if cambio > 0 else "green"
                title_background = "#f8d7da" if cambio > 0 else "#d4edda"
                icono = iconos_categorias.get(categoria, "💰")

                st.markdown(
                    f"""
                    <div class="tarjeta">
                        <div class="tarjeta-titulo" style="background-color: {title_background};">
                            {icono} {categoria.replace('_', ' ').capitalize()}
                        </div>
                        <div class="tarjeta-cuerpo">
                            <div>
                                <b style="font-size: 14px;">L {gastos_reales[webApp_categorias[categoria]]:.2f}</b><br>
                                <span style="font-size: 12px;">Hoy</span>
                            </div>
                            <div>
                                <span style="color: {color}; font-size: 14px; font-weight: bold;">{cambio:.2f}% de cambio</span>
                            </div>
                            <div>
                                <b style="font-size: 14px;">L {prediccion:.2f}</b><br>
                                <span style="font-size: 12px;">Predicción</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )

                # Cerrar el div contenedor
                st.markdown("</div>", unsafe_allow_html=True)
