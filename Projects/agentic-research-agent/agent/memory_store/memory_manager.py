from src.embedder import get_embeddings
from agent.memory_store.vector_memory import VectorMemory

memory = VectorMemory()


def store_memory(text):

    embedding = get_embeddings([text])[0]

    memory.add(embedding, text)


def retrieve_memory(query):

    embedding = get_embeddings([query])[0]

    return memory.search(embedding)