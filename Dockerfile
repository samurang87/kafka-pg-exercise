FROM python:3.11.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN mkdir /app
RUN mkdir /app/certs

COPY . /app

WORKDIR /app

RUN apt-get update \
    && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python - --version 1.2.2

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY . /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction
