FROM python:3.13

WORKDIR /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=False
ENV POETRY_NO_INTERACTION=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi && rm -rf $POETRY_CACHE_DIR

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]