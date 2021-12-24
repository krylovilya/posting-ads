FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y git gcc libpq-dev postgresql-client
RUN pip install poetry && poetry config virtualenvs.create false

COPY ./server/pyproject.toml /server/
COPY ./server/poetry.lock /server/

RUN poetry install

COPY ./server /server
