from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)


def chunk_text(file_content: bytes):
    """
    Splits the given file content into smaller chunks.
    """
    return splitter.create_documents([file_content.decode()])
