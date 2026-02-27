import numpy as np
from openai import OpenAI
import os
from src.cosine_similarity import cosine_similarity

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=os.getenv("OLLAMA_API_KEY")
)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Split text into overlapping chunks.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def retrieve_relevant_chunks(query, chunks, chunk_embeddings, max_chars=20000):
    query_embedding = get_embedding(query)

    scores = []
    for i, emb in enumerate(chunk_embeddings):
        score = cosine_similarity(query_embedding, emb)
        scores.append((score, chunks[i]))

    scores.sort(reverse=True, key=lambda x: x[0])

    selected = []
    total_chars = 0

    for score, chunk in scores:
        if total_chars + len(chunk) > max_chars:
            break
        selected.append(chunk)
        total_chars += len(chunk)

    return "\n\n---\n\n".join(selected)

def get_embedding(text:str) -> np.ndarray:
    """
    Takes a string as input and returns its embedding as a NumPy array.
    An embedding is a list of numbers that represents the meaning of text.
    """

    text = text.replace("\n", " ")

    response = client.embeddings.create(
        model = "qwen3-vl:235b-cloud",
        input = text
    )

    embedding = response.data[0].embedding
    return np.array(embedding)