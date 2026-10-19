
import numpy as np

from src.embeddings import embed_chunks


class FakeEmbeddingModel:
    def encode(
        self,
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ):
        return np.array([
            [0.1, 0.2, 0.3] for _ in texts
        ])


def test_embed_chunks_preserves_metadata():
    chunks = [{
        "chunk_index": 0,
        "page_number": 2,
        "text": "Machine learning learns from data.",
    }]

    result = embed_chunks(chunks, model=FakeEmbeddingModel())

    assert len(result) == 1
    assert result[0]["chunk_index"] == 0
    assert result[0]["page_number"] == 2
    assert result[0]["text"] == "Machine learning learns from data."
    assert result[0]["embedding"] == [0.1, 0.2, 0.3]


def test_empty_chunks_return_empty_list():
    assert embed_chunks([]) == []
