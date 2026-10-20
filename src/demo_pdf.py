
from src.pdf_loader import extract_pdf_text


PDF_PATH = "data/The Psychology of Money.pdf"

def main():
    pages = extract_pdf_text(PDF_PATH)

    print(f"Total text-containing pages: {len(pages)}")

    for page in pages[:3]:
        print(f"\n--- Page {page['page_number']} ---")
        print(page["text"][:500])


if __name__ == "__main__":
    main()
