#imagen de Python y distro linux que vamos a usar
FROM python:3.11.9-bullseye


# Copia todo lo del directorio en el contenedor
COPY . /app


# Establece el directorio de trabajo en el contenedor
WORKDIR /app


# Corre comandos
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Expone puerto
EXPOSE 5005


# OPCIÓN 1
ENV FLASK_APP=app/__init__.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["sh","run.sh"]


# OPCIÓN 2 SENCILLA
# ENTRYPOINT [ "python" ]


# CMD [ "app.py" ] ["sh","run.sh"]


