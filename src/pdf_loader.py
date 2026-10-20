
from pathlib import Path

import pymupdf


def extract_pdf_text(pdf_path: str | Path) -> list[dict]:
    """Extract non-empty text from a PDF, preserving page numbers."""
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The input file must be a PDF.")

    pages = []

    with pymupdf.open(path) as document:
        if document.is_encrypted:
            raise ValueError("The PDF is encrypted.")

        for page_number, page in enumerate(document, start=1):
            text = page.get_text().strip()

            if text:
                pages.append({
                    "page_number": page_number,
                    "text": text,
                })

    if not pages:
        raise ValueError(
            "No readable text found. The PDF may be empty or scanned."
        )

    return pages
