from contextlib import asynccontextmanager

from fastapi import FastAPI
from db.client import WeaviateClient
from routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to manage the lifespan of the app
    """

    await WeaviateClient.connect()
    try:
        yield
    finally:
        await WeaviateClient.close()


app = FastAPI(lifespan=lifespan, title="RAG Backend API")

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["root"])
async def read_root() -> dict:
    """
    Root endpoint"""
    return {"message": "Welcome to the RAG Backend API!"}
