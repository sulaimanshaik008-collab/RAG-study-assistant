
from sentence_transformers import SentenceTransformer

from src.pdf_loader import extract_pdf_text
from src.chunking import chunk_pages
from src.embeddings import embed_chunks
from src.retrieval import retrieve_chunks


PDF_PATH = "data/The Psychology of Money.pdf"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    # Step 1: Extract text from the PDF
    pages = extract_pdf_text(PDF_PATH)
    print(f"Pages extracted: {len(pages)}")

    # Step 2: Split the text into chunks
    chunks = chunk_pages(pages, chunk_size=500, overlap=80)
    print(f"Chunks created: {len(chunks)}")

    # Step 3: Load the embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Step 4: Create embeddings
    embedded_chunks = embed_chunks(chunks, model=model)
    print(f"Embeddings created: {len(embedded_chunks)}")

    # Step 5: Ask a question
    question = input("\nAsk a question about the book: ")

    # Step 6: Retrieve relevant passages
    results = retrieve_chunks(
        query=question,
        embedded_chunks=embedded_chunks,
        model=model,
        top_k=3,
    )

    print("\nMost relevant passages:\n")

    for result in results:
        print(f"Page: {result['page_number']}")
        print(f"Similarity: {result['similarity']:.3f}")
        print(f"Text: {result['text']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
