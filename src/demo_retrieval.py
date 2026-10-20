
from sentence_transformers import SentenceTransformer

from src.embeddings import embed_chunks
from src.retrieval import retrieve_chunks


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    # Example syllabus passages
    chunks = [
        {
            "chunk_index": 0,
            "page_number": 1,
            "text": (
                "Machine learning enables computers to learn "
                "patterns from training data."
            ),
        },
        {
            "chunk_index": 1,
            "page_number": 2,
            "text": (
                "Database management systems store, organize, "
                "and retrieve structured information."
            ),
        },
        {
            "chunk_index": 2,
            "page_number": 3,
            "text": (
                "Computer networks connect devices to exchange "
                "information and resources."
            ),
        },
        {
            "chunk_index": 3,
            "page_number": 4,
            "text": (
                "Operating systems manage computer memory, "
                "processes, and hardware resources."
            ),
        },
        {
            "chunk_index": 4,
            "page_number": 5,
            "text": (
                "Retrieval augmented generation finds relevant "
                "documents to help an AI answer questions."
            ),
        },
    ]

    model = SentenceTransformer(MODEL_NAME)

    embedded_chunks = embed_chunks(chunks, model=model)

    question = "How can computers learn patterns from examples?"

    results = retrieve_chunks(
        query=question,
        embedded_chunks=embedded_chunks,
        model=model,
        top_k=3,
    )

    print(f"\nStudent question: {question}\n")
    print("Most relevant passages:\n")

    for result in results:
        print(f"Page: {result['page_number']}")
        print(f"Similarity: {result['similarity']:.3f}")
        print(f"Text: {result['text']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
