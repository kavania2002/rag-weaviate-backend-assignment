import asyncio

from fastapi import UploadFile
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from db.client import WeaviateClient

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)

# Later on moved as a worker task
async def generate_embeddings(file: UploadFile):
    text = await file.read()  # Read file content
    text_parts = splitter.create_documents([text.decode()])  # Create Documents

    tasks = [
        WeaviateClient.add_file_embedding(
            chunk_content=doc.page_content,
            file_name=file.filename,
            file_type=file.content_type,
            file_embedding=embeddings.embed_query(doc.page_content),
        )
        for doc in text_parts
    ]
    await asyncio.gather(*tasks)
