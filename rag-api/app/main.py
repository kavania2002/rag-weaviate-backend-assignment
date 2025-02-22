from contextlib import asynccontextmanager

from fastapi import FastAPI
from services.db import WeaviateClient
from services.cache import RedisClient
from routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to manage the lifespan of the app
    """

    await WeaviateClient.connect()
    RedisClient.connect()
    try:
        yield
    finally:
        await WeaviateClient.close()
        RedisClient.close()


app = FastAPI(lifespan=lifespan, title="RAG Backend API")

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["root"])
async def read_root() -> dict:
    """
    Root endpoint"""
    return {"message": "Welcome to the RAG Backend API!"}
