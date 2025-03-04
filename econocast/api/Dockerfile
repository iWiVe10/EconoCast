# Usa la versión específica de Python que necesitas
FROM python:3.10.6

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios del proyecto
COPY requirements.txt /app/requirements.txt
COPY setup.py /app/setup.py
COPY econocast /app/econocast

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .


# Comando para lanzar el servidor de FastAPI cuando se inicia el contenedor
CMD ["sh", "-c", "uvicorn econocast.api.fast:app --host 0.0.0.0 --port 8000"]
