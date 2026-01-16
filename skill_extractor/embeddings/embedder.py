from typing import List
import numpy as np


class Embedder:
    """
    Embeds text chunks into fixed-size vectors.
    Embeddings are used ONLY for retrieval.
    """

    def __init__(self, model_name: str = "gemini-embedding"):
        self.model_name = model_name

    def embed(self, chunks: List[str]) -> np.ndarray:
        """
        Returns an in-memory numpy array of embeddings.
        One vector per chunk, index-aligned.
        """
        if not chunks:
            return np.array([])

        # Placeholder deterministic embedding
        # (to be replaced with Gemini embeddings later)
        embeddings = []

        for chunk in chunks:
            # Deterministic hash-based vector (NO semantics)
            vector = np.array(
                [hash(chunk) % 1000], dtype=float
            )
            embeddings.append(vector)

        return np.vstack(embeddings)
