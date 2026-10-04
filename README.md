# FastAPI Deep Dive

An ongoing learning project for exploring FastAPI from the fundamentals to
production-oriented patterns. The codebase will grow incrementally as new
concepts are studied, keeping each example small and practical.

## Topics

- Application and router structure
- Path parameters, query parameters, and request bodies
- Validation and serialization with Pydantic
- Dependencies and configuration
- Error handling and middleware
- Authentication and authorization
- Async code and database integration
- Testing, logging, debugging, and deployment

The current database stack is SQLAlchemy 2, Alembic, Psycopg, and PostgreSQL.

## Requirements

- Docker Compose or Podman Compose for the complete containerized application
- Python 3.14 and [uv](https://docs.astral.sh/uv/) for local development

## Run the complete application in containers

```bash
podman compose up -d --build
```

With Docker, use:

```bash
docker compose up -d --build
```

Compose starts PostgreSQL, applies all pending Alembic migrations, and then
starts the API. PostgreSQL is exposed to the host on port `5433`; containers
communicate with it internally on port `5432`.

View logs or stop the complete stack with:

```bash
podman compose logs -f api
podman compose down
```

## Run the API locally

Start only PostgreSQL and apply migrations:

```bash
uv sync
podman compose up -d db
uv run alembic upgrade head
```

The application entry point is configured in `pyproject.toml`, so no file path
is required:

```bash
uv run fastapi dev
```

The default local connection is
`postgresql+psycopg://postgres:postgres@localhost:5433/fast_api`. Override it
with the `DATABASE_URL` environment variable when needed.

Useful URLs:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Health check: <http://127.0.0.1:8000/health>

Use verbose mode to see application discovery and additional startup details:

```bash
uv run fastapi dev --verbose
```

## Item CRUD

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/items/` | Create an item |
| `GET` | `/items/` | List items |
| `GET` | `/items/{item_id}` | Read one item |
| `PATCH` | `/items/{item_id}` | Update an item |
| `DELETE` | `/items/{item_id}` | Delete an item |

Example request:

```bash
curl -X POST http://127.0.0.1:8000/items/ \
  -H 'Content-Type: application/json' \
  -d '{"name":"Keyboard","description":"Mechanical","price":"99.90"}'
```

## Database migrations

SQLAlchemy models describe the database tables, and Pydantic schemas validate
the API input and output. Alembic tracks changes to the PostgreSQL schema.

After changing a SQLAlchemy model, generate and review a migration:

```bash
uv run alembic revision --autogenerate -m "describe the change"
```

Apply all pending migrations:

```bash
uv run alembic upgrade head
```

Roll back the latest migration:

```bash
uv run alembic downgrade -1
```

Stop the containers without deleting PostgreSQL data:

```bash
podman compose down
```

## Debugging

Run `fast_api.main:app` as a Uvicorn module in your IDE debugger and set
`PYTHONPATH` to the `src` directory. Avoid auto-reload while debugging because
the additional process can interfere with breakpoints.

To trigger a breakpoint in the item endpoint, start the debugger and request:

```text
http://127.0.0.1:8000/items/42?q=hello
```

## Run tests

```bash
uv run python -m unittest -v
```

## Project structure

```text
.
├── pyproject.toml
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── migrations/
│   ├── env.py
│   └── versions/
├── src/
│   └── fast_api/
│       ├── __init__.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       └── routers/
│           ├── __init__.py
│           ├── health.py
│           └── items.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

Additional modules will be added when their related topic is introduced rather
than being scaffolded in advance.

## Status

This project is a work in progress. Its structure and examples will evolve as
the FastAPI deep dive continues.
