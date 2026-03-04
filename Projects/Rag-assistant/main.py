from src.chunking import chunk_text
from src.embedder import get_embeddings
from src.vector_store import create_faiss_index
from src.rag_pipeline import run_rag

# Load docs
with open("data/sample_docs.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Chunk documents
chunks = chunk_text(text)

# Create embeddings
embeddings = get_embeddings(chunks)

# Build FAISS index
index = create_faiss_index(embeddings)

# Query loop
while True:

    question = input("\nAsk a question: ")

    answer, sources = run_rag(index, chunks, question)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources:\n")

    for s in sources:
        print("-", s[:120])