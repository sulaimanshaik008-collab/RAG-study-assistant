import fitz
import pytest

from src.pdf_loader import extract_pdf_text


def test_extracts_text_and_page_numbers(tmp_path):
    pdf_path = tmp_path / "syllabus.pdf"

    with fitz.open() as document:
        page1 = document.new_page()
        page1.insert_text((72, 72), "Introduction to AI")

        page2 = document.new_page()
        page2.insert_text((72, 72), "Machine Learning Basics")

        document.save(pdf_path)

    result = extract_pdf_text(pdf_path)

    assert len(result) == 2
    assert result[0]["page_number"] == 1
    assert "Introduction to AI" in result[0]["text"]
    assert result[1]["page_number"] == 2
    assert "Machine Learning Basics" in result[1]["text"]


def test_missing_pdf_raises_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_pdf_text(tmp_path / "missing.pdf")


def test_empty_pdf_raises_error(tmp_path):
    pdf_path = tmp_path / "empty.pdf"

    with fitz.open() as document:
        document.new_page()
        document.save(pdf_path)

    with pytest.raises(ValueError, match="No readable text"):
        extract_pdf_text(pdf_path)