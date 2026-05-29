# Указываем базовый образ
FROM python:3.12.3

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем poetry
RUN pip install poetry

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./

# Отключаем создание отдельного venv
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["sh", "-c", "python manage.py migrate"]