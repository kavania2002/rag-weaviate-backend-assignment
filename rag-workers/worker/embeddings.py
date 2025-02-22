from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def generate_embedding(text: str):
    """
    Generates an embedding for a given text chunk.
    """
    return embeddings.embed_query(text)
