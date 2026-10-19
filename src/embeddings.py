
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def embed_chunks(chunks: list[dict], model=None) -> list[dict]:
    """Convert text chunks into numerical vectors."""

    if not chunks:
        return []

    if model is None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    results = []

    for chunk, vector in zip(chunks, vectors):
        results.append({
            "chunk_index": chunk["chunk_index"],
            "page_number": chunk["page_number"],
            "text": chunk["text"],
            "embedding": vector.tolist(),
        })

    return results
