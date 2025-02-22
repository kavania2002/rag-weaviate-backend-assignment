from fastapi import APIRouter
from .file import router as file_router
from .health import router as health_router
from .query import router as query_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(file_router, prefix="/file", tags=["file"])
router.include_router(query_router, prefix="/query", tags=["query"])
