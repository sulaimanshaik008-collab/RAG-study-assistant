def chunk_pages(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 80,
) -> list[dict]:
    """Split extracted PDF pages into smaller, overlapping text chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be at least zero and smaller than chunk_size."
        )

    chunks = []

    for page in pages:
        page_number = page["page_number"]
        text = page["text"].strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Prefer a word boundary near the end of the chunk.
            if end < len(text):
                boundary = text.rfind(" ", start + chunk_size // 2, end)

                if boundary > start:
                    end = boundary

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_index": len(chunks),
                    "page_number": page_number,
                    "text": chunk_text,
                })

            if end >= len(text):
                break

            # Move backward to preserve some context for the next chunk.
            next_start = end - overlap

            # Ensure the loop always makes progress.
            start = max(start + 1, next_start)

    return chunks
