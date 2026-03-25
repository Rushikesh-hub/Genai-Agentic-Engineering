from src.ingestion import build_index
from src.rag_pipeline import run_rag

# Load RAG system once
index, chunks = build_index("data/documents")


def rag_agent(query):

    answer, sources = run_rag(index, chunks, query)

    return f"{answer}\n\nSources:\n" + "\n".join([s["source"] for s in sources])