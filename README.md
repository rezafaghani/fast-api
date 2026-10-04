# Fast API

## Setup

```bash
uv sync
```

## Run locally

```bash
uv run fastapi dev src/fast_api/main.py
```

Open <http://127.0.0.1:8000/docs> for the interactive API documentation.

## Run tests

```bash
uv run python -m unittest
```

## Project structure

```text
src/fast_api/
├── main.py          # Creates and configures the application
└── routers/         # HTTP endpoints grouped by feature
tests/               # Automated API tests
```

Add modules such as `database.py`, `models.py`, or `config.py` only when the
application actually needs a database, persisted models, or configuration.
