
import pytest

from src.retrieval import cosine_similarity, retrieve_chunks


class FakeQueryModel:
    def encode(
        self,
        text,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ):
        return [1.0, 0.0]


def test_identical_vectors_have_similarity_one():
    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)


def test_perpendicular_vectors_have_similarity_zero():
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


def test_retrieve_chunks_ranks_best_match_first():
    chunks = [
        {
            "chunk_index": 0,
            "page_number": 1,
            "text": "An unrelated topic.",
            "embedding": [0.0, 1.0],
        },
        {
            "chunk_index": 1,
            "page_number": 2,
            "text": "A matching topic.",
            "embedding": [1.0, 0.0],
        },
    ]

    results = retrieve_chunks(
        "student question",
        chunks,
        model=FakeQueryModel(),
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["text"] == "A matching topic."
    assert results[0]["page_number"] == 2
    assert results[0]["similarity"] == pytest.approx(1.0)


def test_empty_chunks_return_empty_results():
    assert retrieve_chunks(
        "student question",
        [],
        model=FakeQueryModel(),
    ) == []


def test_vectors_must_have_same_dimensions():
    with pytest.raises(ValueError):
        cosine_similarity([1, 0], [1, 0, 1])
