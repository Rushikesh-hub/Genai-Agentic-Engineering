import faiss
import numpy as np

def create_faiss_index(embeddings):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)

    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)

    return index