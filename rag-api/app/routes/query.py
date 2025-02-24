import uuid
import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from controllers.query import QueryController
from utils.response import is_json_serialized

router = APIRouter()


@router.post("/{file_id}")
async def query(file_id: str, search_query: str):
    """
    Query File Endpoint
    """

    query_id = uuid.uuid4().hex
    QueryController.query_file(query_id, file_id, search_query)
    return JSONResponse({"message": "Query processing started", "query_id": query_id})


@router.get("/status/{query_id}")
async def get_query_status(query_id: str):
    """
    Get Query Status Endpoint
    """
    response = await QueryController.get_query_status(query_id)
    if is_json_serialized(response):
        response = json.loads(response)
    return JSONResponse(
        {"message": "Query status", "result": response if response else "Not found"}
    )
