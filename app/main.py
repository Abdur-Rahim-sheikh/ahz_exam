from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.database import create_db_and_tables
from .routers.db import router as dbRouter


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="AHZ database", lifespan=lifespan)

app.include_router(dbRouter, prefix="/api/query")
