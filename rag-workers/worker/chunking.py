import io
import json
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    RecursiveJsonSplitter,
)
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx

splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
json_splitter = RecursiveJsonSplitter(max_chunk_size=512)


def extract_text_unstructured_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts text from a PDF using the Unstructured library.
    """
    # TODO: for completion of task, had to use ocr (facing some issue in hi_res) and need to find some other way to extract text from pdf
    elements = partition_pdf(
        file=io.BytesIO(pdf_bytes),
        strategy="ocr_only",
        infer_table_structure=True,
    )

    if not elements or len(elements) == 0:
        raise ValueError("No text found in the PDF file.")

    raw_texts = [element.text for element in elements if element.text]
    return "\n".join(raw_texts)


def extract_text_unstructured_from_docx(docx_bytes: bytes) -> str:
    """
    Extracts text from a Docx using the Unstructured library.
    """
    elements = partition_docx(
        file=io.BytesIO(docx_bytes),
        strategy="fast",
        infer_table_structure=True,
        include_page_breaks=True,
    )
    if not elements or len(elements) == 0:
        raise ValueError("No text found in the Docx file.")

    raw_texts = [element.text for element in elements]
    return "\n".join(raw_texts)


def extract_text_from_json(json_bytes: bytes):
    """
    Extracts text from JSON by flattening it.
    """
    try:
        json_data = json.loads(json_bytes.decode())

        if isinstance(json_data, dict):
            json_data = [json_data]

        if not isinstance(json_data, list):
            raise ValueError("JSON must be an array of objects.")

        return json_data

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}") from e


def chunk_text(file_content: bytes, file_type: str):
    """
    Splits the given file content into smaller chunks.
    """
    if file_type == "txt":
        return splitter.create_documents([file_content.decode()])

    if file_type == "json":
        json_data = extract_text_from_json(file_content)
        return json_splitter.create_documents(json_data)

    if file_type == "pdf":
        full_text = extract_text_unstructured_from_pdf(file_content)
        print(f"Full extracted text:\n{full_text[:500]}...")
        return splitter.create_documents([full_text])

    if file_type == "docx":
        full_text = extract_text_unstructured_from_docx(file_content)
        print(f"Full extracted text:\n{full_text[:500]}...")
        return splitter.create_documents([full_text])
