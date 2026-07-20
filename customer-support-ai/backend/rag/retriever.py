# RAG retriever - ties together the embeddings module and the FAISS vector store
# so agents can just call retriever.retrieve(query) and get back relevant chunks

from backend.embeddings.embedder import load_and_chunk_documents, embed_texts, embed_query
from backend.vectorstore.faiss_store import FaissStore


class Retriever:
    def __init__(self):
        self.store = FaissStore()
        self._build_index()

    def _build_index(self):
        print("[RAG] Loading documents from knowledge_base/ ...")
        chunks, sources = load_and_chunk_documents()

        if not chunks:
            print("[RAG] WARNING: no documents found in knowledge_base/")
            return

        print("[RAG] Generating embeddings...")
        embeddings = embed_texts(chunks)
        self.store.build(chunks, sources, embeddings)
        print(f"[RAG] Indexed {len(chunks)} chunks from {len(set(sources))} documents.")

    def retrieve(self, query: str, top_k: int = 3):
        query_vec = embed_query(query)
        return self.store.search(query_vec, top_k)


# built once when the server starts up
retriever = Retriever()
