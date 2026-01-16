from typing import List, Tuple
import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Computes cosine similarity between two vectors.
    """
    if np.linalg.norm(a) == 0.0 or np.linalg.norm(b) == 0.0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def top_k_similar(
    embeddings: np.ndarray,
    query_embedding: np.ndarray,
    chunks: List[str],
    k: int = 3
) -> List[Tuple[int, str, float]]:
    """
    Returns top-k most similar chunks based on cosine similarity.
    Output: (chunk_index, chunk_text, similarity_score)
    """
    if embeddings.size == 0 or query_embedding.size == 0:
        return []

    scores = []

    for idx, emb in enumerate(embeddings):
        score = cosine_similarity(emb, query_embedding)
        scores.append((idx, chunks[idx], score))

    # Sort by similarity DESC, index ASC for determinism
    scores.sort(key=lambda x: (-x[2], x[0]))

    return scores[:k]
