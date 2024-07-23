FROM python:3.11.2

WORKDIR /usr/src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VENV_PATH=".venv"

COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 8000