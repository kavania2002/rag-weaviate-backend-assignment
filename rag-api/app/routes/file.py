from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from processing.embeddings import generate_embeddings, query_embeddings

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
    file_id = await generate_embeddings(file)

    return JSONResponse(
        {"message": "File stored and processing started", "file_id": file_id}
    )


@router.get("/query")
async def query_file(file_id: str, query: str):
    """
    Query File Endpoint
    """
    response = await query_embeddings(file_id, query)
    # add task to celery queue
    # query embeddings
    return JSONResponse({"message": "Query processed", "data": response})
