FROM python:3.13

WORKDIR /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=False
ENV POETRY_NO_INTERACTION=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --no-interaction --no-ansi --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Используем официальный образ Nginx
FROM nginx:latest

# Копируем файл конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем статические файлы веб-сайта в директорию для обслуживания
COPY html/ /usr/share/nginx/html/

# Открываем порт 80 для HTTP-трафика
EXPOSE 80
