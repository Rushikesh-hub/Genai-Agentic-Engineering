from fastapi import FastAPI
from pydantic import BaseModel

from src.chunking import chunk_text
from src.embedder import get_embeddings
from src.vector_store import create_faiss_index
from src.rag_pipeline import run_rag

# Load docs once at startup
with open("data/sample_docs.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(text)
embeddings = get_embeddings(chunks)
index = create_faiss_index(embeddings)

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "RAG API running"}


@app.post("/ask")
def ask_question(request: QueryRequest):

    answer, sources = run_rag(index, chunks, request.question)

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }