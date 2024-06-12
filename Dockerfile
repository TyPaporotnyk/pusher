FROM python:3.12-alpine as python

FROM python as python-build-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apk update && apk add --no-cache \
  build-base \
  py3-cryptography \
  py3-mysqlclient \
  mariadb-dev \
  build-base \
  freetype-dev \
  tzdata

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/

RUN poetry run python manage.py migrate && poetry run python manage.py collectstatic --noinput
