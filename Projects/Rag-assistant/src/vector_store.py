import faiss
import numpy as np
import os


def create_faiss_index(embeddings):

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    vectors = np.array(embeddings).astype("float32")

    index.add(vectors)

    return index


def save_index(index, path="vector_store/faiss_index"):

    os.makedirs("vector_store", exist_ok=True)

    faiss.write_index(index, path)


def load_index(path="vector_store/faiss_index"):

    return faiss.read_index(path)