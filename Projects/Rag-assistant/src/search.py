import numpy as np


def search(index, query_embedding, top_k=5):

    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    return indices[0]