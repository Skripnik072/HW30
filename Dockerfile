FROM python:3.13

WORKDIR /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE = False

COPY pyproject.toml poetry.lock ./

COPY . .

RUN pip install celery
RUN pip install django-celery-beat

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]