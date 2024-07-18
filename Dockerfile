FROM python:3.11.2

WORKDIR /src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VENV_PATH=".venv"

COPY certs/ certs/
RUN pip freeze > requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app src 