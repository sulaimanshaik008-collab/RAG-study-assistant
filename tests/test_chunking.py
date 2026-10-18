
import pytest

from src.chunking import chunk_pages


def test_short_text_creates_one_chunk():
    pages = [
        {"page_number": 1, "text": "Introduction to Artificial Intelligence"}
    ]

    chunks = chunk_pages(pages, chunk_size=100, overlap=10)

    assert len(chunks) == 1
    assert chunks[0]["page_number"] == 1
    assert "Artificial Intelligence" in chunks[0]["text"]


def test_long_text_creates_multiple_chunks():
    pages = [
        {"page_number": 2, "text": "word " * 200}
    ]

    chunks = chunk_pages(pages, chunk_size=100, overlap=20)

    assert len(chunks) > 1
    assert all(len(chunk["text"]) <= 100 for chunk in chunks)
    assert all(chunk["page_number"] == 2 for chunk in chunks)


def test_empty_page_is_skipped():
    pages = [
        {"page_number": 1, "text": "   "}
    ]

    assert chunk_pages(pages) == []


def test_invalid_overlap_raises_error():
    pages = [{"page_number": 1, "text": "Example text"}]

    with pytest.raises(ValueError):
        chunk_pages(pages, chunk_size=100, overlap=100)


def test_chunks_have_unique_indexes():
    pages = [{"page_number": 1, "text": "word " * 200}]

    chunks = chunk_pages(pages, chunk_size=100, overlap=20)
    indexes = [chunk["chunk_index"] for chunk in chunks]

    assert len(indexes) == len(set(indexes))
