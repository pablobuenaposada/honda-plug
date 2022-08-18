FROM python:3.10.4

WORKDIR /app

COPY src /app/src
COPY Makefile requirements.txt requirements-tests.txt docker-compose.yml pyproject.toml .env.test /app/

RUN make venv
