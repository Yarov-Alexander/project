FROM python:3.12-slim

# чтобы логи сразу выводились
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# системные зависимости (для asyncpg/psycopg)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# сначала зависимости (кэш Docker)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# копируем код (но НЕ .env благодаря .dockerignore)
COPY . .

# порт
EXPOSE 8000

# запуск через uvicorn (без хардкода env)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]