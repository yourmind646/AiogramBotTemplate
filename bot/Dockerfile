# базовый образ Python
FROM python:3.13-alpine

# рабочая директория
WORKDIR /app

# файл зависимостей
COPY bot/requirements.txt /app/

# устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./bot /app
