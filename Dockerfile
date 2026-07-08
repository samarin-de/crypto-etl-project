# 1. Базовый образ с Python
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл со скриптом
COPY fetch_prices.py .

# 4. Устанавливаем зависимости
RUN pip install requests psycopg2-binary

# 5. Команда по умолчанию: запустить скрипт
CMD ["python", "fetch_prices.py"]
