from typing import Dict, List

from preprocessing.cleaner import clean_text
from preprocessing.splitter import split_text
from preprocessing.chunker import create_chunks

from embeddings.embedder import Embedder
from vector_store.similarity import top_k_similar

from extractor.skill_parser import extract_skills_from_chunks
from extractor.normalizer import normalize_and_deduplicate
from output.formatter import format_output


def run_skill_extraction_pipeline(
    raw_text: str,
    query_text: str = "",
    top_k: int = 3
) -> Dict[str, List[str]]:
    """
    End-to-end skill extraction pipeline.
    """
    # 1. Preprocessing
    cleaned = clean_text(raw_text)
    sentences = split_text(cleaned)
    chunks = create_chunks(sentences)

    # 2. Embeddings (retrieval only)
    embedder = Embedder()
    chunk_embeddings = embedder.embed(chunks)

    # Query embedding (use query_text if provided, else empty string)
    query = query_text if query_text else ""
    query_embedding = embedder.embed([query])[0] if chunks else []

    # 3. Vector retrieval
    retrieved = top_k_similar(
        embeddings=chunk_embeddings,
        query_embedding=query_embedding,
        chunks=chunks,
        k=top_k
    )

    # Extract only retrieved chunk texts
    retrieved_chunks = [chunk for _, chunk, _ in retrieved]

    # 4. Strict extraction
    extracted = extract_skills_from_chunks(retrieved_chunks)

    # 5. Normalization + deduplication
    normalized = normalize_and_deduplicate(extracted)

    # 6. Final formatting
    final_output = format_output(normalized)

    return final_output
