FROM ghcr.io/blindfoldedsurgery/poetry:2.0.0-pipx-3.12-bullseye

COPY [ "poetry.toml", "poetry.lock", "pyproject.toml", "README.md", "./" ]
COPY src/kw src/kw

RUN poetry install --only main


ENTRYPOINT [ "poetry", "run", "python", "-m", "kw" ]
