# # Etapa única: Runtime com TensorFlow e dependências Python

# # FROM tensorflow/tensorflow:2.15.0
# FROM jupyter/tensorflow-notebook:x86_64-python-3.11

# WORKDIR /app

# # Copia requirements e instala dependências
# COPY requirements.txt .
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # Copia o restante do app
# COPY . .

# # Expondo a porta usada pelo Flask
# EXPOSE 5000

# # Entrypoint (ajuste se quiser usar gunicorn ou uvicorn)
# CMD ["python", "src/main.py"]

# Etapa única: Python 3.11 + TensorFlow 2.16.1 + dependências do projeto

FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema para compilar pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala TensorFlow 2.16.1 (primeira versão oficial com suporte a Python 3.11)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tensorflow==2.16.1

# Copia requirements e instala dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir --ignore-installed -r requirements.txt

# Copia o restante do app
COPY . .

EXPOSE 5000

CMD ["python", "src/main.py"]