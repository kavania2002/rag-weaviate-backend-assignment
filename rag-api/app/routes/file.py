import uuid

from fastapi import APIRouter, UploadFile, BackgroundTasks, status, HTTPException
from fastapi.responses import JSONResponse
from controllers.file import FileController
from services.embeddings import query_embeddings

from utils.constants import ALLOWED_FILE_TYPES, MAX_FILE_SIZE

router = APIRouter()


@router.post("/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile):
    """
    Upload File Endpoint
    """
    if not file:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No file provided"
        )

    # Can check mimetype here but for simplicity we will check the file extension
    file_extension = file.filename.split(".")[-1]
    if file_extension not in ALLOWED_FILE_TYPES:
        return HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported Media Type",
        )

    if file.size > MAX_FILE_SIZE:
        return HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size too large",
        )

    file_content = await file.read()
    if not file_content:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No file content"
        )
    file_id = uuid.uuid4().hex

    # need to sync read the file content
    background_tasks.add_task(
        FileController.upload_file, file_id, file_content, file.filename, file_extension
    )

    return JSONResponse(
        {"message": "File processing started", "file_id": f"{file_id}.{file_extension}"}
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


@router.get("/status")
async def get_status(file_id: str):
    """
    Get File Status Endpoint
    """
    response = await FileController.get_file_status(file_id)
    return JSONResponse(
        {
            "message": "File status retrieved",
            "data": response if response else "File not found",
        }
    )
