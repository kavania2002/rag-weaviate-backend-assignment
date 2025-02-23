from sentence_transformers import SentenceTransformer

embeddings = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")


def generate_embedding(text: str):
    """
    Generates an embedding for a given text chunk.
    """
    return embeddings.encode(text).tolist()
