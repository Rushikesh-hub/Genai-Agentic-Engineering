from src.loader import load_documents
from src.chunking import semantic_chunk_documents
from src.embedder import get_embeddings
from src.vector_store import create_faiss_index


def build_index(doc_folder):

    documents = load_documents(doc_folder)

    chunks = semantic_chunk_documents(documents)

    texts = [c["text"] for c in chunks]

    embeddings = get_embeddings(texts)

    index = create_faiss_index(embeddings)

    return index, chunks