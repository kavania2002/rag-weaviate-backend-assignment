from fastapi import FastAPI
from routes import router as api_router

app = FastAPI(title="RAG Backend API")

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["root"])
async def read_root() -> dict:
    """
    Root endpoint"""
    return {"message": "Welcome to the RAG Backend API!"}
