
import math


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Measure how similar two vectors are."""

    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions.")

    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_chunks(
    query: str,
    embedded_chunks: list[dict],
    model,
    top_k: int = 3,
) -> list[dict]:
    """Return the chunks most similar to a student's question."""

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not embedded_chunks:
        return []

    query_vector = model.encode(
        query,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    if hasattr(query_vector, "tolist"):
        query_vector = query_vector.tolist()

    results = []

    for chunk in embedded_chunks:
        score = cosine_similarity(
            query_vector,
            chunk["embedding"],
        )

        result = chunk.copy()
        result["similarity"] = score
        results.append(result)

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return results[:top_k]
