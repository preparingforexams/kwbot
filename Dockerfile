FROM python:3.12-slim

WORKDIR /app/build

RUN pip install poetry==1.7.0

WORKDIR /app

RUN poetry config virtualenvs.create false

COPY [ "poetry.toml", "poetry.lock", "pyproject.toml", "./" ]

RUN poetry install --only main

COPY bot/ bot/
COPY main.py main.py

ENTRYPOINT [ "python", "main.py" ]
