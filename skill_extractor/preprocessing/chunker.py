def create_chunks(sentences: list[str], max_sentences: int = 5) -> list[str]:
    """
    Creates structure-aware chunks using headers as hard boundaries.
    A header is any sentence ending with ':'.
    """
    if not sentences:
        return []

    chunks = []
    current_chunk = []

    for sentence in sentences:
        # Header detected
        if sentence.endswith(":"):
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
            current_chunk.append(sentence)
            continue

        current_chunk.append(sentence)

        if len(current_chunk) >= max_sentences:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
