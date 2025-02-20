from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from processing.embeddings import generate_embeddings

from utils.constants import ALLOWED_FILE_TYPES

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile):
    """
    Upload File Endpoint
    """
    if file.filename.split(".")[-1] not in ALLOWED_FILE_TYPES:
        return HTTPException(status_code=415, detail="Unsupported Media Type")

    # upload file to s3
    # add task to celery queue
    await generate_embeddings(file)

    return JSONResponse({"message": "File stored and processing started"})

