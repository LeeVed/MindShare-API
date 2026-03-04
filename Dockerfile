FROM python:3.13-slim

WORKDIR /app
# устанавливаем пакеты и очищаем кэш после установки
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
# Устанавливаем Poetry (меньше размер образа)
RUN pip install --no-cache-dir poetry
# Копируем файлы зависимостей
COPY poetry.lock pyproject.toml ./
# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
# Копируем код (откуда -> куда)
COPY . .

EXPOSE 8000
# Запускаем
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
