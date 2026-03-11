from src.ingestion import build_index
from src.embedder import get_embeddings
from src.search import search


index, chunks = build_index("data/documents")


questions = [
    "What is generative AI?",
    "Explain embeddings",
    "What is retrieval augmented generation?",
    "Explain agentic AI systems"
]


for q in questions:

    print("\nQUESTION:", q)

    emb = get_embeddings([q])[0]

    results = search(index, emb)

    for r in results:

        print("-", chunks[r]["text"][:120])