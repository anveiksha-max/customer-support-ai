# loads PDFs from knowledge_base/, splits into chunks, and turns them into embeddings
# using sentence-transformers (all-MiniLM-L6-v2)

import os
import glob
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

KB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge_base")
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

_model = SentenceTransformer("all-MiniLM-L6-v2")


def _extract_pdf_text(filepath: str) -> str:
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    # simple fixed-size sliding window chunking, good enough for our doc sizes
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if c]


def load_and_chunk_documents():
    """Reads every PDF in knowledge_base/ and returns (chunks, sources) lists."""
    chunks = []
    sources = []
    for filepath in glob.glob(os.path.join(KB_DIR, "*.pdf")):
        filename = os.path.basename(filepath)
        text = _extract_pdf_text(filepath)
        for chunk in _chunk_text(text):
            chunks.append(chunk)
            sources.append(filename)
    return chunks, sources


def embed_texts(texts):
    """Turns a list of text chunks into embedding vectors."""
    return _model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def embed_query(query: str):
    """Embeds a single query string the same way as the documents."""
    return _model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
