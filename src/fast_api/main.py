from fastapi import FastAPI

from fast_api.routers import health, items

app = FastAPI(title="Fast API", version="0.1.0")

app.include_router(health.router)
app.include_router(items.router)
