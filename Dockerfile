# Базовый образ — используем стабильную версию Python
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    postgresql-client \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry (официальный способ)
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Отключаем виртуальные окружения от Poetry, чтобы использовать системное
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальной код проекта
COPY . .

# Указываем команду запуска (опционально, пример для Django)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
