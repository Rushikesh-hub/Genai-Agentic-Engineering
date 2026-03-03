from src.chunking import chunk_text
from src.embedder import get_embeddings
from src.vector_store import create_faiss_index
from src.search import search

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load document
with open("data/sample_docs.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Chunk
chunks = chunk_text(text)

# Embed chunks
embeddings = get_embeddings(chunks)

# Create FAISS index
index = create_faiss_index(embeddings)

# Query
query = "What is Retrieval Augmented Generation?"
query_embedding = get_embeddings([query])[0]

results = search(index, query_embedding)

print("Top relevant chunks:")
for idx in results:
    print("\n---")
    print(chunks[idx])
    