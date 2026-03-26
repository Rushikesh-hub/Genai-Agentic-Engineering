import faiss
import numpy as np

class VectorMemory:

    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embedding, text):
        vector = np.array([embedding]).astype("float32")
        self.index.add(vector)
        self.texts.append(text)

    def search(self, embedding, top_k=3):
        vector = np.array([embedding]).astype("float32")
        distances, indices = self.index.search(vector, top_k)

        results = []

        for i in indices[0]:
            if i < len(self.texts):
                results.append(self.texts[i])

        return results