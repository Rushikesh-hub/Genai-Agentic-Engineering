import os
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# RAG modules
from src.chunking import chunk_text
from src.embedder import get_embeddings
from src.vector_store import create_faiss_index
from src.rag_pipeline import run_rag
from src.ingestion import build_index


index, chunks = build_index("data/documents")
# Load environment variables
load_dotenv()

# -----------------------------
# Logging Setup
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------
# FastAPI App
# -----------------------------

app = FastAPI(
    title="RAG Knowledge Assistant API",
    description="Retrieval-Augmented Generation API for answering questions from internal documents",
    version="1.0"
)

# -----------------------------
# Request Schema
# -----------------------------

class QueryRequest(BaseModel):
    question: str


# -----------------------------
# Load Documents (Startup)
# -----------------------------

try:

    logger.info("Loading knowledge base...")

    with open("data/sample_docs.txt", "r", encoding="utf-8") as f:
        text = f.read()

    logger.info("Chunking documents...")

    chunks = chunk_text(text)

    logger.info(f"Total chunks created: {len(chunks)}")

    logger.info("Generating embeddings...")

    embeddings = get_embeddings(chunks)

    logger.info("Creating FAISS index...")

    index = create_faiss_index(embeddings)

    logger.info("RAG system initialized successfully")

except Exception as e:
    logger.error("Failed to initialize RAG system")
    logger.error(str(e))
    raise e


# -----------------------------
# Health Endpoint
# -----------------------------

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "RAG Knowledge Assistant API"
    }


# -----------------------------
# Ask Endpoint
# -----------------------------

@app.post("/ask")
def ask_question(request: QueryRequest):

    try:

        logger.info(f"Question received: {request.question}")

        answer, sources = run_rag(index, chunks, request.question)

        return {
            "question": request.question,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        logger.error("Error processing request")
        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )