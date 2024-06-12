FROM python:3.10.9

WORKDIR /app

COPY src /app/src
COPY Makefile poetry.toml poetry.lock docker-compose.yml pyproject.toml .env.test /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false # to install dependencies system wide and not in a venv
RUN make venv
