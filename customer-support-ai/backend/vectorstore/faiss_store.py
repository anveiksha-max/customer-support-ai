# FAISS vector store - stores the chunk embeddings and does similarity search

import numpy as np
import faiss


class FaissStore:
    def __init__(self):
        self.index = None
        self.chunks = []
        self.sources = []

    def build(self, chunks, sources, embeddings):
        self.chunks = chunks
        self.sources = sources
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # normalized vectors -> inner product = cosine sim
        self.index.add(embeddings.astype(np.float32))

    def search(self, query_vec, top_k: int = 3):
        if self.index is None or not self.chunks:
            return []
        scores, indices = self.index.search(query_vec.astype(np.float32), top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "text": self.chunks[idx],
                "source": self.sources[idx],
                "score": float(score),
            })
        return results
