import numpy as np

def cosine_similarity(A, B):
    """
    Compute cosine similarity between two vectors.

    For 2 similar vectors A and B
    cosine similarity= dot(A, B) / (norm(A) * norm(B))
    Where dot is the dot product and norm is the length of the vector

    Range of cosine similarity is [-1, 1]

    In embeddings:
    Similar sentences → ~0.7 to 0.95
    Unrelated → ~0 to 0.3
    Opposite concepts → can go negative
    
    """
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))