import asyncio
import uuid

from fastapi import UploadFile
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from db.client import WeaviateClient

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)


# Later on moved as a worker task
async def generate_embeddings(file: UploadFile):
    text = await file.read()
    text_parts = splitter.create_documents([text.decode()])

    file_id = uuid.uuid4().hex
    tasks = [
        WeaviateClient.add_file_embedding(
            file_id=file_id,
            chunk_content=doc.page_content,
            file_name=file.filename,
            file_type=file.content_type,
            file_embedding=embeddings.embed_query(doc.page_content),
        )
        for doc in text_parts
    ]
    await asyncio.gather(*tasks)
    return file_id


async def query_embeddings(file_id: str, query: str):
    query_vector = embeddings.embed_query(query)
    response = await WeaviateClient.query_file_embeddings(file_id, query_vector)
    return response
