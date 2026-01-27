from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from .models import engine
from .routers.db import router as dbRouter


@asynccontextmanager
async def lifespan(_app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="AHZ database", lifespan=lifespan)

app.include_router(dbRouter, prefix="/api/query")
